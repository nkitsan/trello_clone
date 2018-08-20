from django.test import TestCase
from tasker.libs.managers import user_manager
from django.contrib.auth.hashers import make_password, check_password
from tasker.models import User


class TaskManagerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='example', email='examle@post.com',
                                        password_hash=make_password('1111'))

    def test_signup_user(self):
        self.assertTrue(user_manager.signup_user('tester', 'tester@tester.com', '111111'))
        self.assertFalse(user_manager.signup_user(self.user.username, 'some@some.com', '123456a'))
        self.assertFalse(user_manager.signup_user('unique_username', self.user.email, '123456a'))

    def test_login(self):
        self.assertTrue(user_manager.login_user(self.user.username, '1111'))
        self.assertFalse(user_manager.login_user(self.user.username, '11111'))
        self.assertFalse(user_manager.login_user('shuser', '1111'))
