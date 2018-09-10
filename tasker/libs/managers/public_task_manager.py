"""
This manager controls server-side work with a data and responsible for changing tasks in userlists
"""


from tasker.models import User, List, PublicTask, Task
from .task_manager import *
from tasker.libs.logger.logger import get_logs, configure_logging


@get_logs
def create_public_list(username, list_name):
    """
    Creates a new list

    :param username: an username of an user
    :param list_name: a name of a new list
    :return: an essence of a new list
    """
    user = User.objects.get(username=username)
    return user.lists.create(name=list_name)


@get_logs
def create_public_task(username, list_id, task_name):
    """
    Creates a new task in list

    :param username: an username of an user
    :param list_id: an id of a list to add a task
    :param task_name: a name of a new task
    :return: an essence of a new task
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    return public_list.tasks.create(task=create_task(task_name))


@get_logs
def delete_public_list(username, list_id):
    """
    Deletes a list

    :param username: an username of an user
    :param list_id: an id of a list to delete
    """
    user = User.objects.get(username=username)
    user.lists.filter(id=list_id).delete()


@get_logs
def delete_public_task(username, list_id, task_id):
    """
    Deletes a task in a list

    :param username: an username of an user
    :param list_id: an id of a list to delete a task in it
    :param task_id: an id of task to delete
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    delete_task(task.task)
    task.delete()


@get_logs
def change_public_list_name(username, list_id, new_name):
    """
    Changes a list name

    :param username: an username of an user
    :param list_id: an id of a lis to change name
    :param new_name: a new name of list
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    public_list.name = new_name
    public_list.save()


@get_logs
def change_public_task_name(username, list_id, task_id, new_name):
    """
    Changes a task name in a list

    :param username: an username of an user
    :param list_id: an id of a list to change a task in it
    :param task_id: an id of a task to change it
    :param new_name: a new name of a task
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    edit_task_name(task.task, new_name)


@get_logs
def change_public_task_status(username, list_id, task_id, status):
    """
    Changes a task status in a list

    :param username: an username of an user
    :param list_id: an id of a list to change task in it
    :param task_id: an id of a task to change
    :param status: a new status
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    change_status(task.task, status)


@get_logs
def add_public_task_comment(username, list_id, task_id, comment):
    """
    Adds a new comment to task in a list

    :param username: an username of an user
    :param list_id: an id of a list
    :param task_id: an id of a task to add a comment
    :param comment: a text of a new comment
    :return: an essence of a new comment
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    return add_comment(task.task, comment)


@get_logs
def delete_public_task_comment(username, list_id, task_id, comment_id):
    """
    Deletes comment from a task in a list

    :param username: an username of an user
    :param list_id: an id of a list
    :param task_id: an id of a task in a list
    :param comment_id: an id of a comment to delete
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    delete_comment(task.task, comment_id)


@get_logs
def change_public_task_comment(username, list_id, task_id, comment_id, new_text):
    """
    Changes a comment text in a task

    :param username: an username of an user
    :param list_id: an id of a list
    :param task_id: an id of a task in a list
    :param comment_id: an id of a comment to change
    :param new_text: a new text of comment
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    change_comment(task.task, comment_id, new_text)


@get_logs
def add_public_task_subtask(username, list_id, task_id, subtask):
    """
    Adds a new subtask for a task in alist

    :param username: an username of an user
    :param list_id: an id of a list
    :param task_id: an id of a task in a list to add a subtask
    :param subtask: a title of a new subtask
    :return: an essence of a new  subtask
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    return add_subtask(task.task, subtask)


@get_logs
def delete_public_task_subtask(username, list_id, task_id, subtask_id):
    """
    Deletes a subtask from a task in a list

    :param username: an username of an user
    :param list_id: an id of a list
    :param task_id: an id of a task in a list to delete a subtask
    :param subtask_id: id of a subtask to delete
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    delete_subtask(task.task, subtask_id)


@get_logs
def change_public_task_subtask(username, list_id, task_id, subtask_id, new_subtask):
    """
    Changes a name af a subtask in a task of a list

    :param username: an username of an user
    :param list_id: an id of a list
    :param task_id: an id of a task in a list to change a subtask
    :param subtask_id: id of a subtask to change
    :param new_subtask: a new name of a subtask
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    change_subtask(task.task, subtask_id, new_subtask)


@get_logs
def change_public_task_subtask_status(username, list_id, task_id, subtask_id, status):
    """
    Changes a status of a subtask

    :param username: an username of an user
    :param list_id: an id of a list
    :param task_id: an id of a task in a list to change a subtask
    :param subtask_id: id of a subtask to change
    :param status: a new status of a subtask
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    change_subtask_status(task.task, subtask_id, status)


@get_logs
def change_public_task_deadline(username, list_id, task_id, deadline):
    """
    Changes a deadline in a task

    :param username: an username of an user
    :param list_id: an id of a list
    :param task_id: an id of a task in a list
    :param deadline: a new value of a deadline
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    change_deadline(task.task, deadline)


@get_logs
def delete_public_task_deadline(username, list_id, task_id):
    """
    Deletes a deadline from a task in a list

    :param username: an username of an user
    :param list_id: an id of a list
    :param task_id: an id of a task in a list
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    delete_deadline(task.task)


@get_logs
def add_public_list_user(username, new_username, list_id):
    """
    Adds an user access to a list

    :param username: an username of an user
    :param new_username: an username of an user to provide an access
    :param list_id: an id of a list to provide an access
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    if User.objects.filter(username=new_username).exists():
        new_user = User.objects.get(username=new_username)
        new_user.lists.add(public_list)


@get_logs
def delete_public_list_user(username, remove_username, list_id):
    """
    Deletes an user access to a list

    :param username: an username of an user
    :param remove_username: n username of an user to delete an access
    :param list_id: an id of a list to delete an access
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    if User.objects.filter(username=remove_username).exists():
        remove_user = User.objects.get(username=remove_username)
        remove_user.lists.remove(public_list)


@get_logs
def add_task_executor(username, executor_username, list_id, task_id):
    """
    Adds an executor of a task in a list

    :param username: an username of an user
    :param executor_username: an username of executor
    :param list_id: an id of a list
    :param task_id: an id of a task in a list
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    if User.objects.filter(username=executor_username).exists() and not task.executors.filter(username=executor_username).exists():
        executor_user = User.objects.get(username=executor_username)
        task.executors.add(executor_user)


@get_logs
def delete_task_executor(username, executor_username, list_id, task_id):
    """
    Deletes an executor of a task in a list

    :param username: an username of an user
    :param executor_username: an username of executor
    :param list_id: an id of a list
    :param task_id: an id of a task in a list
    """
    user = User.objects.get(username=username)
    public_list = user.lists.get(id=list_id)
    task = public_list.tasks.get(id=task_id)
    if task.executors.filter(username=executor_username).exists():
        remove_user = User.objects.get(username=executor_username)
        task.executors.remove(remove_user)


@get_logs
def get_user_lists(username):
    """
    Returns all lists of an user

    :param username: an username of an user
    :return: an array of an user lists essences
    """
    user = User.objects.get(username=username)
    return user.lists.all()


@get_logs
def get_user_list(username, list_id):
    """
    Returns an user list by id

    :param username: an username of an user
    :param list_id: an id of an user list
    :return: an essence of a list or None if a list with a such id does not exist
    """
    user = User.objects.get(username=username)
    if not user.lists.filter(id=list_id).exists():
        return None
    return user.lists.get(id=list_id)


@get_logs
def get_list_tasks(username, list_id):
    """
    Returns tasks from a list

    :param username: an username of an user
    :param list_id: an id of an user list
    :return: an array of tasks essences or None if a list with a such id does not exist
    """
    user = User.objects.get(username=username)
    if not user.lists.filter(id=list_id).exists():
        return None
    list = user.lists.get(id=list_id)
    return list.tasks.all()


@get_logs
def get_list_task(username, list_id, task_id):
    """
    Returns a task from a list

    :param username: an username of an user
    :param list_id: an id of an user list
    :param task_id: an id of a task in a list
    :return: a task essence or None if a list or a task does not exist
    """
    tasks = get_list_tasks(username, list_id)
    if tasks is None:
        return None
    if not tasks.filter(id=task_id).exists():
        return None
    return tasks.get(id=task_id)