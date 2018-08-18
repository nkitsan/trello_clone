"""
This manager organises work with users such as registration of new users and login
"""


from tasker.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist


def signup_user(username, email, password):
    user = User.objects.create(username=username, email=email, password_hash=make_password(password))
    user.generate_api_key()
    user.save()


def login(username, password):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return False
    return check_password(password, user.password_hash)


def get_username(api_key):
    try:
        user = User.objects.get(api_key=api_key)
    except ObjectDoesNotExist:
        return None
    return user.username