from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def main_page(request):
    return render(request, 'index.html')