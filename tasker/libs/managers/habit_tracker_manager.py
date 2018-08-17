"""
Manager for adding, deleting and changing habits in the habit tracker
"""


from tasker.models import User, Habit
from .task_manager import *


def create_habit(username, habit_name):
    user = User.objects.get(username=username)
    habits = user.habit_tracker.habits
    habits.create(name=habit_name)


def set_habit_timeline(username, habit_name, timeline):
    user = User.objects.get(username=username)
    habit = user.habit_tracker.habits.get(name=habit_name)
    habit.timeline = timeline
    habit.save()


def change_habit_status(username, habit_name, status):
    user = User.objects.get(username=username)
    habit = user.habit_tracker.habits.get(name=habit_name)
    habit.status = status
    habit.save()


def change_habit_name(username, new_name, old_name):
    user = User.objects.get(username=username)
    habit = user.habit_tracker.habits.get(name=old_name)
    habit.name = new_name
    habit.save()


def delete_habit(username, habit_name):
    user = User.objects.get(username=username)
    habit = user.habit_tracker.habits.get(name=habit_name)
    habit.delete()
