from django.test import TestCase
from tasker.libs.managers import task_manager
from tasker.models import Task, Comment, Subtask
from datetime import timedelta
import datetime


class TaskManagerTestCase(TestCase):

    def setUp(self):
        self.task = task_manager.create_task('test task')

    def test_edit_task(self):
        task_manager.edit_task_name(self.task, 'new name test task')
        self.assertEqual(self.task.name, 'new name test task')

    def test_delete_task(self):
        task_manager.delete_task(self.task)
        self.assertNotIn(self.task, Task.objects.all())

    def test_add_comment(self):
        test_comment = 'this is text of comment for task'
        task_manager.add_comment(self.task, test_comment)
        comment = Comment.objects.get(comment=test_comment)
        self.assertIn(comment, self.task.comments.all())

    def test_delete_comment(self):
        test_comment = 'this is text of comment for task'
        task_manager.add_comment(self.task, test_comment)
        comment = Comment.objects.get(comment=test_comment)
        task_manager.delete_comment(self.task, comment.id)
        self.assertNotIn(comment, self.task.comments.all())

    def test_change_status(self):
        task_manager.change_status(self.task, 'F')
        self.assertEqual(self.task.status, 'F')

    def test_add_subtask(self):
        subtask_name = 'test subtask'
        task_manager.add_subtask(self.task, subtask_name)
        subtask = Subtask.objects.get(name=subtask_name)
        self.assertIn(subtask, self.task.subtasks.all())

    def test_change_subtask_name(self):
        subtask_name = 'test subtask'
        subtask = task_manager.add_subtask(self.task, subtask_name)
        new_name = 'new subtask name'
        task_manager.change_subtask(self.task, subtask.id, new_name)
        subtask = self.task.subtasks.get(id=subtask.id)
        self.assertEqual(subtask.name, new_name)

    def test_change_subtask_status(self):
        subtask_name = 'test subtask'
        subtask = task_manager.add_subtask(self.task, subtask_name)
        task_manager.change_subtask_status(self.task, subtask.id, 'F')
        subtask = self.task.subtasks.get(id=subtask.id)
        self.assertEqual(subtask.status, 'F')

    def test_set_deadline(self):
        deadline = datetime.datetime.now() + datetime.timedelta(days=7)
        task_manager.change_deadline(self.task, deadline)
        self.assertEqual(self.task.deadline, deadline)

    def test_delete_deadline(self):
        task_manager.delete_deadline(self.task)
        self.assertIsNone(self.task.deadline)