"""
This manager controls server-side work with a data and responsible for changing tasks in userlists
"""
from tasker.models import Task, Subtask, Comment
from tasker.libs.logger.logger import get_logs


@get_logs
def create_task(name):
    """
    Creates a new task

    :param name: a name of a new task
    :return: a task essence
    """
    task = Task.objects.create(name=name)
    return task


@get_logs
def edit_task_name(task, new_name):
    """
    Edits a task name

    :param task: an essence of a task
    :param new_name: a value of a new name
    """
    task.name = new_name
    task.save()


@get_logs
def delete_task(task):
    """
    Deletes a task

    :param task: an essence of a task
    """
    Task.objects.filter(id=task.id).delete()


@get_logs
def add_comment(task, text):
    """
    Adds a comment to a task

    :param task: an essence of a task
    :param text: text of a new comment
    :return: an essence of a comment
    """
    return task.comments.create(comment=text)


@get_logs
def change_comment(task, comment_id, new_text):
    """
    Edits a text in a comment

    :param task: an essence of a task
    :param comment_id: an id of a comment to edit
    :param new_text: a new value of a comment text
    """
    comment = task.comments.get(id=comment_id)
    comment.comment = new_text
    comment.save()


@get_logs
def delete_comment(task, comment_id):
    """
    Deletes a comment

    :param task: an essence of a task
    :param comment_id: an id of a comment to delete
    """
    task.comments.filter(id=comment_id).delete()


@get_logs
def change_status(task, status):
    """
    Changes a status of task

    :param task: an essence of a task
    :param status: a new value of status
    """
    task.status = status
    task.save()


@get_logs
def add_subtask(task, name):
    """
    Creates a subtask

    :param task: an essence of a task
    :param name: a name of a new subtask
    :return: a subtask essence
    """
    return task.subtasks.create(name=name)


@get_logs
def change_subtask(task, subtask_id, new_subtask_name):
    """
    Changes a subtask name

    :param task: an essence of a task
    :param subtask_id: an id of a subtask to change
    :param new_subtask_name: a new value of a subtask name
    """
    subtask = task.subtasks.get(id=subtask_id)
    subtask.name = new_subtask_name
    subtask.save()
    task.save()


@get_logs
def delete_subtask(task, subtask_id):
    """
    Deletes a subtask

    :param task: an essence of a task
    :param subtask_id: an id of a subtask to delete
    """
    task.subtasks.filter(id=subtask_id).delete()


@get_logs
def change_subtask_status(task, subtask_id, status):
    """
    Changes a subtask status

    :param task: an essence of a task
    :param subtask_id: an id of a subtask to change
    :param status: a new value of a status
    """
    subtask = task.subtasks.get(id=subtask_id)
    subtask.status = status
    subtask.save()


@get_logs
def change_deadline(task, deadline):
    """
    Changes a deadline of a task

    :param task: an essence of a task
    :param deadline: a new value of a deadline
    """
    task.deadline = deadline
    task.save()


@get_logs
def delete_deadline(task):
    """
    Deletes a deadline of a task

    :param task: an essence of a task
    """
    task.deadline = None
    task.save()

