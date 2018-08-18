from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
import json
from tasker.libs.managers.user_manager import *


def login(request):
    if request.method == "GET":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is not None and request is not None and login_user(username, password):
            return redirect('user_board')
        else:
            return render(request, 'tasker/login.html')
    else:
        return render(request, 'tasker/login.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if signup_user(username, email, password):
            return redirect('user_board')
    else:
        return render(request, 'tasker/signup.html')


def user_board(request):
    render(request, 'tasker/index.html')