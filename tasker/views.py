from django.shortcuts import render


def login(request):
    return render(request, 'tasker/login.html', {})


def signup(request):
    return render(request, 'tasker/signup.html', {})