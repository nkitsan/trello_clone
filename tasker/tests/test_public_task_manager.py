from django.test import TestCase
from tasker.libs.managers import weekly_task_manager
from django.contrib.auth.hashers import make_password, check_password
from tasker.models import User, Task
import datetime


class TaskManagerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='example', email='examle@post.com',
                                        password_hash=make_password('1111'))
        self.task = Task.objects.create(name='my test task')
        self.list = User.objects.lists.create(name='public list')
        self.private_task = self.user.week_list.create(task=self.task)