"""
Manager for adding, deleting and changing tasks in weekly tasks list
"""


from tasker.models import User
from .task_manager import *
from tasker.libs.logger.logger import get_logs


@get_logs
def add_weeklytask(username, task_name):
    """
    Adds a new task in the weekly tasks

    :param username: an username of an user
    :param task_name: a name of a new task
    :return: an essence of a task
    """
    user = User.objects.get(username=username)
    task = create_task(task_name)
    return user.week_list.create(task=task)


@get_logs
def change_weeklytask_name(username, task_id, new_name):
    """
    Changes a name of a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to change
    :param new_name: a new value of a task name
    """
    task = find_user_task(username, task_id)
    edit_task_name(task.task, new_name)


@get_logs
def delete_weeklytask(username, task_id):
    """
    Deletes a task from the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to delete
    """
    task = find_user_task(username, task_id)
    delete_task(task.task)
    task.delete()


@get_logs
def change_weeklytask_status(username, task_id, status):
    """
    Changes a name of a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to change
    :param status: a new value of a status
    """
    task = find_user_task(username, task_id)
    change_status(task.task, status)


@get_logs
def add_weeklytask_comment(username, task_id, comment):
    """
    Adds a new comment to a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to add a comment
    :param comment: a text of a new comment
    :return: an essence of a comment
    """
    task = find_user_task(username, task_id)
    return add_comment(task.task, comment)


@get_logs
def change_weeklytask_comment(username, task_id, comment_id, new_text):
    """
    Changes a comment of a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to change a comment
    :param comment_id: an id of a comment to change
    :param new_text: a text of a changed comment
    """
    task = find_user_task(username, task_id)
    change_comment(task.task, comment_id, new_text)


@get_logs
def delete_weeklytask_comment(username, task_id, comment_id):
    """
    Deletes a comment of a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to delete a comment
    :param comment_id: an id of a comment to delete
    """
    task = find_user_task(username, task_id)
    delete_comment(task.task, comment_id)


@get_logs
def add_weeklytask_subtask(username, task_id, subtask_name):
    """
    Adds a subtask to a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to add a subtask
    :param subtask_name: a name value of a subtask
    :return: an essence of a subtask
    """
    task = find_user_task(username, task_id)
    return add_subtask(task.task, subtask_name)


@get_logs
def change_weeklytask_subtask(username, task_id, subtask_id, new_name):
    """
    Changes a subtask name of a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to change a subtask
    :param subtask_id: an id of a subtask to change
    :param new_name: a value of a new subtask name
    """
    task = find_user_task(username, task_id)
    change_subtask(task.task, subtask_id, new_name)


@get_logs
def change_weeklytask_subtask_status(username, task_id, subtask_id, status):
    """
    Changes a subtask status of a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to change a subtask
    :param subtask_id: an id of a subtask to change
    :param status: a new value of status
    """
    task = find_user_task(username, task_id)
    change_subtask_status(task.task, subtask_id, status)


@get_logs
def delete_weeklytask_subtask(username, task_id, subtask_id):
    """
    Deletes a subtask of a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to delete a subtask
    :param subtask_id: an id of a subtask to delete
    """
    task = find_user_task(username, task_id)
    delete_subtask(task.task, subtask_id)


@get_logs
def change_weeklytask_deadline(username, task_id, deadline):
    """
    Changes a deadline of a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to change a deadline
    :param deadline: a new value of a deadline
    """
    task = find_user_task(username, task_id)
    change_deadline(task.task, deadline)


@get_logs
def delete_weeklytask_deadline(username, task_id):
    """
    Deletes a deadline of a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to delete a deadline
    """
    task = find_user_task(username, task_id)
    delete_deadline(task.task)


@get_logs
def add_weeklytask_repeat(username, task_id, repeat):
    """
    Adds a weekly repeat

    :param username: an username of an user
    :param task_id: an id of a task to add a repeat
    :param repeat:
    :return: an essence of a repeat
    """
    task = find_user_task(username, task_id)
    if not task.repeat.filter(repeat=repeat).exists() and 0 <= int(repeat) < 7:
        return task.repeat.create(repeat=repeat)
    return None


@get_logs
def delete_weeklytask_repeat(username, task_id, repeat_id):
    """
    Deletes a repeat of task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to delete a repeat
    :param repeat_id: an id of a repeat to delete
    """
    task = find_user_task(username, task_id)
    task.repeat.filter(id=repeat_id).delete()


@get_logs
def add_weeklytask_remember(username, task_id, remember):
    """
    Adds a remember for a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to add a remember
    :param remember: a date of a remember
    :return: an essence of new remember
    """
    task = find_user_task(username, task_id)
    return task.remember.create(repeat_date=remember)


@get_logs
def delete_weeklytask_remember(username, task_id, remember_id):
    """
    Deletes a remember for a task in the weekly tasks

    :param username: an username of an user
    :param task_id: an id of a task to delete a remember
    :param remember_id: an id of a remember to delete
    :return:
    """
    task = find_user_task(username, task_id)
    task.remember.filter(id=remember_id).delete()


@get_logs
def find_user_task(username, task_id):
    """
    Finds an user task

    :param username: an username of an user
    :param task_id: an id of a task to find
    :return: an essence of a task or None if task was not found
    """
    user = User.objects.get(username=username)
    if not user.week_list.filter(id=task_id).exists():
        return None
    return user.week_list.get(id=task_id)


@get_logs
def get_weekly_tasks(username):
    """
    Returns all tasks of an user

    :param username: an username of an user
    :return: an array of tasks essences
    """
    user = User.objects.get(username=username)
    return user.week_list.all()