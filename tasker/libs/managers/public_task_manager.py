"""
This manager controls server-side work with a data and responsible for changing tasks in userlists
"""


from tasker.models import User, List, PublicTask, Task
from .task_manager import *


def create_public_list(username, list_name):
    user = User.objects.get(username=username)
    return user.lists.create(name=list_name)


def create_public_task(username, list_id, task_name):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    return public_list.tasks.create(task=create_task(task_name))


def delete_public_list(username, list_id):
    user = User.objects.get(username=username)
    user.lists.filter(id=list_id).delete()


def delete_public_task(username, list_id, task_id):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    delete_task(task.task)
    task.delete()


def change_public_list_name(username, list_id, new_name):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    public_list.name = new_name
    public_list.save()


def change_public_task_name(username, list_id, task_id, new_name):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    edit_task_name(task.task, new_name)


def change_public_task_status(username, list_id, task_id, status):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    change_status(task.task, status)


def add_public_task_comment(username, list_id, task_id, comment):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    return add_comment(task.task, comment)


def delete_public_task_comment(username, list_id, task_id, comment_id):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    delete_comment(task.task, comment_id)


def change_public_task_comment(username, list_id, task_id, comment_id, new_text):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    change_comment(task.task, comment_id, new_text)


def add_public_task_subtask(username, list_id, task_id, subtask):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    return add_subtask(task.task, subtask)


def delete_public_task_subtask(username, list_id, task_id, subtask_id):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    delete_subtask(task.task, subtask_id)


def change_public_task_subtask(username, list_id, task_id, subtask_id, new_subtask):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    change_subtask(task.task, subtask_id, new_subtask)


def change_public_task_subtask_status(username, list_id, task_id, subtask_id, status):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    change_subtask_status(task.task, subtask_id, status)


def change_public_task_deadline(username, list_id, task_id, deadline):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    change_deadline(task.task, deadline)


def delete_public_task_deadline(username, list_id, task_id):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    delete_deadline(task.task)


def add_public_list_user(username, new_username, list_id):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    new_user = User.objects.get(username=new_username)
    new_user.lists.add(public_list)


def delete_public_list_user(username, remove_username, list_id):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    remove_user = User.objects.get(username=remove_username)
    remove_user.lists.remove(public_list)


def add_task_executor(username, executor_username, list_id, task_id):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    executor_user = User.objects.get(username=executor_username)
    task.executors.add(executor_user)


def delete_task_executor(username, executor_username, list_id, task_id):
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    remove_user = User.objects.get(username=executor_username)
    task.executors.remove(remove_user)


def get_user_lists(username):
    user = User.objects.get(username=username)
    return user.lists.all()


def get_user_list(username, list_id):
    user = User.objects.get(username=username)
    if not user.lists.filter(id=list_id).exists():
        return None
    return user.lists.get(id=list_id)


def get_list_tasks(username, list_id):
    user = User.objects.get(username=username)
    if not user.lists.filter(id=list_id).exists():
        return None
    list = user.lists.get(id=list_id)
    return list.tasks.all()


def get_list_task(username, list_id, task_id):
    tasks = get_list_tasks(username, list_id)
    if tasks is None:
        return None
    if not tasks.filter(id=task_id).exists():
        return None
    return tasks.get(id=task_id)