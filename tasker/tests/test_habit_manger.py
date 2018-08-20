from django.test import TestCase
from tasker.libs.managers import habit_tracker_manager
from django.contrib.auth.hashers import make_password, check_password
from tasker.models import User, Habit


class TaskManagerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='example', email='examle@post.com',
                                        password_hash=make_password('1111'))
        self.habit = self.user.habit_tracker.create(name='test habit')

    def test_change_habit_name(self):
        habit_tracker_manager.change_habit_name(self.user.username, self.habit.id, 'new habit name')
        habit = Habit.objects.get(id=self.habit.id)
        self.assertEqual(habit.name, 'new habit name')

    def test_set_habit_timeline(self):
        habit_tracker_manager.set_habit_timeline(self.user.username, self.habit.id, 90)
        habit = Habit.objects.get(id=self.habit.id)
        self.assertEqual(habit.timeline, 90)

    def test_delete_habit(self):
        habit_tracker_manager.delete_habit(self.user.username, self.habit.id)
        self.assertNotIn(self.habit, self.user.habit_tracker.all())