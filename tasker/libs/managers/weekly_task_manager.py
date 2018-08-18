"""
Manager for adding, deleting and changing tasks in weekly tasks list
"""


from tasker.models import User, WeeklyList, PrivateTask
from .task_manager import *


def add_weeklytask(username, task_name):
    user = User.objects.get(username=username)
    tasks = user.week_list.tasks
    task = create_task(task_name)
    tasks.create(task=task)


def change_weeklytask_name(username, task_id, new_name):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    edit_task_name(task.task, new_name)


def delete_weeklytask(username, task_id):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    delete_task(task.task)
    task.delete()


def change_weeklytask_status(username, task_id, status):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    change_status(task.task, status)


def add_weeklytask_comment(username, task_id, comment):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    add_comment(task.task, comment)


def change_weeklytask_comment(username, task_id, comment_id, new_text):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    change_comment(task.task, comment_id, new_text)


def delete_weeklytask_comment(username, task_id, comment_id):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    delete_comment(task.task, comment_id)


def add_weeklytask_subtask(username, task_id, subtask_name):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    add_subtask(task.task, subtask_name)


def change_weeklytask_subtask(username, task_id, subtask_id, new_name):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    change_subtask(task.task, subtask_id, new_name)


def change_weeklytask_subtask_status(username, task_id, subtask_id, status):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    change_subtask_status(task.task, subtask_id, status)


def delete_weeklytask_subtask(username, task_id, subtask_id):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    delete_subtask(task.task, subtask_id)


def change_weeklytask_deadline(username, task_id, deadline):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    change_deadline(task.task, deadline)


def delete_weeklytask_deadline(username, task_id):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    delete_deadline(task.task)


def add_weeklytask_repeat(username, task_id, repeat):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    task.repeat.create(repeat=repeat)


def delete_weeklytask_repeat(username, task_id, repeat):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    task.repeat.delete(repeat=repeat)


def add_weeklytask_remember(username, task_id, remember):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    task.remember.create(remember=remember)


def delete_weeklytask_remember(username, task_id, remember):
    user = User.objects.get(username=username)
    task = user.week_list.tasks.get(id=task_id)
    task.repeat.delete(remember=remember)
