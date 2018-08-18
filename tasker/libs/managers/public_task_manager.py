"""
This manager controls server-side work with a data and responsible for changing tasks in userlists
"""


from tasker.models import User, List, PublicTask, Task
from .task_manager import *


def create_public_list(username, list_name):
    user = User.objects.get(username=username)
    user.lists.create(name=list_name)


def create_public_task(username, list_id, task_name):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    public_list.tasks.create(task=create_task(task_name))


def delete_public_list(username, list_id):
    user = User.objects.get(username=username)
    user.lists.delete(name=list_id)


def delete_public_task(username, list_id, task_id):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    for task in public_list.tasks:
        if task.id == task_id:
            delete_task(task.task)
            task.delete()
            break


def change_public_list_name(username, list_id, new_name):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    public_list.name = new_name
    public_list.save()


def change_public_task_name(username, list_id, task_id, new_name):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    for task in public_list.tasks:
        if task.id == task_id:
            edit_task_name(task.task, new_name)
            break


