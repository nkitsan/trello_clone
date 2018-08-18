"""
This manager organises work with users such as registration of new users and login
"""


from tasker.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist


def signup_user(username, email, password):
    if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
        user = User.objects.create(username=username, email=email, password_hash=make_password(password))
        user.generate_api_key()
        user.save()
        return True
    return False


def login_user(username, password):
    if User.objects.filter(username=username).exists:
        user = User.objects.get(username=username)
        return check_password(password, user.password_hash)
    return False


def get_username(api_key):
    try:
        user = User.objects.get(api_key=api_key)
    except ObjectDoesNotExist:
        return None
    return user.username