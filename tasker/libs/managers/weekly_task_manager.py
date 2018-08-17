"""
Manager for adding, deleting and changing tasks in weekly tasks list
"""


from tasker.models import User, WeeklyList, PrivateTask
from .task_manager import *


def add_weekly_task(username, task_name):
    user = User.objects.get(username=username)
    tasks = user.week_list.tasks
    task = create_task(task_name)
    tasks.create(task=task)


def delete_weekly_task(username, task_name):
    user = User.objects.get(username=username)
    tasks = user.week_list.tasks
    for task in tasks:
        if task.task.name == task_name:
            delete_task(task.task)
            task.delete()
            break


def change_weekly_task():
    pass
