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
        self.private_task = self.user.week_list.create(task=self.task)

    def test_add_weekly_task_repeat(self):
        repeat = weekly_task_manager.add_weeklytask_repeat(self.user.username, self.private_task.id, 0)
        self.assertIn(repeat, self.private_task.repeat.all())

    def test_delete_task_repeat(self):
        repeat = weekly_task_manager.add_weeklytask_repeat(self.user.username, self.private_task.id, 0)
        weekly_task_manager.delete_weeklytask_repeat(self.user.username, self.private_task.id, repeat.id)
        self.assertNotIn(repeat, self.private_task.repeat.all())

    def test_add_task_remember(self):
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        remember = weekly_task_manager.add_weeklytask_remember(self.user.username, self.private_task.id, date)
        self.assertIsNotNone(remember)