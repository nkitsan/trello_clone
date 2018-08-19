from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
import json
from tasker.libs.managers.user_manager import *


def login(request):
    if request.session.get('username') is not None:
        return redirect('user_board', request=request)
    elif request.method == "GET":
        username = request.GET.get('username')
        password = request.GET.get('password')
        if username is not None and request is not None and login_user(username, password):
            request.session['username'] = username
            return redirect('user_board', request=request)
        else:
            return render(request, 'tasker/login.html')
    else:
        return render(request, 'tasker/login.html')


def signup(request):
    if request.session.get('username') is not None:
        return redirect('user_board', request=request)
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if signup_user(username, email, password):
            request.session['username'] = username
            return redirect('/profile/{}/'.format(username))
    else:
        return render(request, 'tasker/signup.html')


def user_board(request, username):
    user = User.objects.get(username=username)
    return render(request, 'tasker/index.html', {'api_key': user.api_key})