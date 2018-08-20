"""
This manager controls server-side work with a data and responsible for changing tasks in userlists
"""
from tasker.models import Task, Subtask, Comment


def create_task(name):
    task = Task.objects.create(name=name)
    return task


def edit_task_name(task, new_name):
    task.name = new_name
    task.save()


def delete_task(task):
    Task.objects.filter(id=task.id).delete()


def add_comment(task, text_of_comment):
    return task.comments.create(comment=text_of_comment)


def change_comment(task, comment_id, new_text):
    comment = task.comments.get(id=comment_id)
    comment.comment = new_text


def delete_comment(task, comment_id):
    task.comments.filter(id=comment_id).delete()


def change_status(task, status):
    task.status = status
    task.save()


def add_subtask(task, name):
    return task.subtasks.create(name=name)


def change_subtask(task, subtask_id, new_subtask_name):
    subtask = task.subtasks.get(id=subtask_id)
    subtask.name = new_subtask_name
    subtask.save()
    task.save()


def delete_subtask(task, subtask_id):
    task.subtasks.filter(id=subtask_id).delete()


def change_subtask_status(task, subtask_id, status):
    subtask = task.subtasks.get(id=subtask_id)
    subtask.status = status
    subtask.save()


def change_deadline(task, deadline):
    task.deadline = deadline
    task.save()


def delete_deadline(task):
    task.deadline = None
    task.save()

