from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from main import forms
from main import utils
from main.models import Game, Rate
import json
# from .models import Users
# Create your views here.
Users = get_user_model()
def main_page(request):
    return render(request, 'index.html')

def reg_page(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        reg_form = forms.reg_form(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            context['username'] = username
            context['password'] = password
        
            
            if Users.objects.filter(username=username).exists():
                print("user exists")
                context['User_exists_error'] = "User already exists"
                context['reg_form'] = forms.reg_form()
                return render(request, 'register.html', context)
            else:
                print("new user")
                user = Users.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                context['user'] = user
                return redirect('/profile')
    else:
        context['reg_form'] = forms.reg_form()

    return render(request, 'register.html', context)

def loginUser(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        reg_form = forms.reg_form(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            context['username'] = username
            context['password'] = password
            print(request.user)
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                print("user exists")
                context['user'] = user
                login(request, user)
                return redirect('/profile')
                
            else:
                context['reg_form'] = forms.reg_form()
                if Users.objects.filter(username=username).exists():
                    context['User_wrong_error'] = "Неправильный пароль"
                else:
                    context['User_wrong_error'] = "Пользователя с таким ником не существует"
                print("new user, wrong credentials or etc")
                return render(request, 'login.html', context)
    else:
        context['reg_form'] = forms.reg_form()


    return render(request, 'login.html', context)

def logoutUser(request):
    if not request.user.is_authenticated:
        return redirect('/')
    context = {}
    if request.method == "POST":
        logout(request)
        return redirect('/login')
    else:
        return render(request, 'logout.html')

def profile(request, name=None):
    context = {}
    if request.method == 'GET':
        if request.user.is_authenticated:
            if name == None or name==request.user.username:
                print(f"name=={name}")
                context = {}
                context['user'] = request.user
                context['user_itself'] = True
                context['username'] = request.user.username
                return render(request, 'profile.html', context)
            else:
                if Users.objects.filter(username=name).exists():
                    needed_user = Users.objects.get(username=name)
                    print("some user found", name)
                    context = {}
                    context['user_itself'] = False
                    context['username'] = name
                    return render(request, 'profile.html', context)
                else:
                    print("user not found")
                    return render(request, 'error.html')
        else:
            return redirect('/login')
    context['username'] = request.user.username
    if request.method != "GET":
        return redirect("/")
    return render(request, "profile.html", context)

def games(request, name=None):
    context = {}
    context['user'] = request.user
    games = Game.objects.all()
    for game in games:
        rating = json.loads(get_rating(request, game.id).content)
        if rating["status"] == "ok":
            game.rating = rating['rating']
        else:
            game.rating = -1
    context['games'] = games
    return render(request, 'games.html', context)
        
@login_required #временно..
def game_page(request, name):
    print(name)
    context = {}
    if name:
        if Game.objects.filter(site_url_name=name).exists():
            game = Game.objects.get(site_url_name=name)
            rating = json.loads(get_rating(request, game.id).content)
            context['game'] = game
            context['rating'] = rating
            if Rate.objects.filter(game=game, user=request.user):
                context['user_rate'] = Rate.objects.get(game=game, user=request.user)
        else:
            context['error'] = "Игра не найдена."
        return render(request, 'gamepage.html', context)
    else:    
        return render(request, 'error.html')
    
@login_required
def add_game(request, name=None):
    context = {}
    context['user'] = request.user
    context['games'] = [{'name': "Minecraft", 'rating': utils.generate_float(1, 10, 1)} for _ in range(10)]
    context['result'] = None
    if request.method == "POST":
        game_form = forms.game_form(request.POST, request.FILES)
        if game_form.is_valid():
            print(game_form.cleaned_data)
            cleaned_data = game_form.cleaned_data
            name = cleaned_data['name']
            site_url_name = utils.generate_site_url_name(name=name)
            short_description = cleaned_data['short_description']
            description = cleaned_data['description']
            icon = cleaned_data['game_icon']
            game_link = cleaned_data['game_link']
            if not Game.objects.filter(site_url_name=site_url_name).exists(): # запасная проверка на повтор, не особо надежная если честно
                game = Game.objects.create(is_active=True,name=name, site_url_name=site_url_name, short_description=short_description, description=description, icon=icon, game_link=game_link, author=request.user)
                game.save()
                context['result'] = "Игра отправлена на модерацию (пока что ее нет, поэтому добавлена на сайт сразу)"
            else:
                context['result'] = "Возможно, игра уже есть на сайте"
    else:
        context['game_form'] = forms.game_form()
    return render(request, 'addgame.html', context)

def rating(request, game_id):
    if request.method == "POST":
        rating_value = request.POST.get('rating')
        if rating_value and str(rating_value).isnumeric():
            mark = min(10, max(1, int(rating_value)))
            
            if not Game.objects.filter(id=game_id).exists():
                return JsonResponse({'status':"error"}, status=400)
            
            game = Game.objects.get(id=game_id)
            user = request.user
            comment = ""
            # TODO: add comments
            if not Rate.objects.filter(game=game, user=user).exists():
                # User hasn't rated this game
                rate = Rate.objects.create(game=game, user=user, mark=mark, comment=comment)
                rate.save()
                print("new rate added")
            else:
                # User re-rating the game
                rate = Rate.objects.get(game=game, user=user)
                rate.mark = mark
                rate.save()
                print("rewriting existing rate")
            return JsonResponse({
                'status':"success",
                "game_id":game_id,
                "user_id":user.id,
                'rating':mark
            })
        else:
            return JsonResponse({
                "status":"error",
                "game_id":game_id
            }, status=400)
            print("что-то не так с оценкой?")
    else:
        return get_rating(request, game_id)
    print("???")
    return JsonResponse({"status":"error", "message":"get-запросы не приветствуются"}, status=405)

def get_rating(request, game_id):
    if request.method == "GET":
        if not Game.objects.filter(id=game_id).exists():
            print("Игра не найдена")
            return JsonResponse({
                "status":"error",
                "game_id":game_id,
                "message":"Game not found"
            })
        game = Game.objects.get(id=game_id)
        ratings = game.ratings.all()
        stats = ratings.aggregate(
            total_sum = Sum('mark'),
            amt = Count("id")
        )
        total_sum = stats['total_sum']
        amount = stats['amt']
        print(total_sum, amount)
        
        return JsonResponse({
            "status":"ok",
            "rating": round(total_sum/amount, 1) if amount > 0 else -1,
            "votes" : amount
        })
        