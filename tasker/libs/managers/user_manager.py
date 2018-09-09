"""
This manager organises work with users such as registration of new users and login
"""


from tasker.models import User
from tasker.libs.logger.logger import get_logs
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist


@get_logs
def signup_user(username, email, password):
    """
    Signups user

    :param username: an username of a user
    :param email: an email of user
    :return: True if user was registered successfully or False if
    user with such email or username exists
    """
    if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
        user = User.objects.create(username=username, email=email, password_hash=make_password(password))
        user.generate_api_key()
        user.save()
        return True
    return False


@get_logs
def login_user(username, password):
    """
    Logins user

    :param username: an username of a user
    :return: True if login process went successfully else return False
    """
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        return check_password(password, user.password_hash)
    return False


@get_logs
def get_username(api_key):
    """
    Returns username

    :param api_key: an api-key from an user profile
    :return: an user username if api-key relates to any user else None
    """
    try:
        user = User.objects.get(api_key=api_key)
    except ObjectDoesNotExist:
        return None
    return user.username


@get_logs
def get_user(username):
    """
    Returns user essence by username

    :param username: an user username
    :return: an user essence if an user with username exists else None
    """
    if User.objects.filter(username=username).exists():
        return User.objects.get(username=username)
    else:
        return None