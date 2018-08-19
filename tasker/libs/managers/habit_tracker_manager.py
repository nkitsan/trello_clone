"""
Manager for adding, deleting and changing habits in the habit tracker
"""


from tasker.models import User, Habit
from .task_manager import *


def create_habit(username, habit_name):
    user = User.objects.get(username=username)
    habits = user.habits
    habits.create(name=habit_name)


def set_habit_timeline(username, habit_id, timeline):
    user = User.objects.get(username=username)
    habit = user.habits.get(id=habit_id)
    habit.timeline = timeline
    habit.save()


def change_habit_status(username, habit_id, status):
    user = User.objects.get(username=username)
    habit = user.habits.get(id=habit_id)
    habit.status = status
    habit.save()


def change_habit_name(username, habit_id, new_name):
    user = User.objects.get(username=username)
    habit = user.habits.get(id=habit_id)
    habit.name = new_name
    habit.save()


def delete_habit(username, habit_id):
    user = User.objects.get(username=username)
    habit = user.habits.get(id=habit_id)
    habit.delete()
