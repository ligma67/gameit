from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from main import forms
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
                    request.user.friends.add()
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
