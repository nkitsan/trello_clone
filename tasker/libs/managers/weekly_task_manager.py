"""
Manager for adding, deleting and changing tasks in weekly tasks list
"""


from tasker.models import User, WeeklyList, PrivateTask
from .task_manager import *


def add_weekly_task(username, task_name):
    user = User.objects.get(username=username)
    tasks = user.week_list.tasks
    task = create_task(task_name)
    tasks.add(task)


def delete_weekly_task(username, task_name):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(name=task_name)
    delete_task(task)


def change_weekly_task():
    pass
