from django.test import TestCase
from tasker.libs.managers import public_task_manager
from django.contrib.auth.hashers import make_password, check_password
from tasker.models import User, List, Task


class TaskManagerTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='example', email='examle@post.com',
                                         password_hash=make_password('1111'))
        self.user2 = User.objects.create(username='exmpl', email='exmpl@post.com', password_hash=make_password('1111'))
        self.list = self.user1.lists.create(name='public list')
        self.task = Task.objects.create(name='my test task')
        self.public_task = self.list.tasks.create(task=self.task)

    def test_add_list_to_user(self):
        public_task_manager.add_public_list_user(self.user1.username, self.user2.username, self.list.id)
        self.assertIn(self.list, self.user2.lists.all())

    def test_add_executor_to_task(self):
        public_task_manager.add_public_list_user(self.user1.username, self.user2.username, self.list.id)
        public_task_manager.add_task_executor(self.user1.username, self.user2.username, self.list.id,
                                              self.public_task.id)
        self.assertIn(self.user2, self.public_task.executors.all())

    def test_delete_list_from_user(self):
        public_task_manager.add_public_list_user(self.user1.username, self.user2.username, self.list.id)
        public_task_manager.delete_public_list_user(self.user1.username, self.user2.username, self.list.id)
        self.assertNotIn(self.list, self.user2.lists.all())
        self.assertTrue(List.objects.filter(id=self.list.id).exists())

    def test_delete_executor_to_task(self):
        public_task_manager.add_task_executor(self.user1.username, self.user2.username, self.list.id,
                                              self.public_task.id)
        public_task_manager.delete_task_executor(self.user1.username, self.user2.username, self.list.id,
                                                 self.public_task.id)
        self.assertNotIn(self.user2, self.public_task.executors.all())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())


    def test_add_comment_to_task(self):
        comment = public_task_manager.add_public_task_comment(self.user1.username, self.list.id, self.public_task.id,
                                                              'text of comment')
        self.assertIn(comment, self.public_task.task.comments.all())