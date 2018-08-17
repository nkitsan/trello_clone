"""
This manager control server-side work with a data and responsible for changing tasks in userlists
"""
from tasker.models import Task, Subtask, Comment


def create_task(name):
    task = Task.objects.create(name=name)
    return task


def edit_task_name(task, new_name):
    task.name = new_name
    task.save()


def delete_task(task):
    task.delete()


def add_comment(task, text_of_comment):
    task.comments.create(comment=text_of_comment)


def change_comment():
    pass


def delete_comment():
    pass


def change_status(task, status):
    task.status = status
    task.save()


def add_subtask(task, name):
    task.subtasks.create(name=name)


def change_subtask(task, new_subtask_name, old_subtask_name):
    subtasks = task.subtasks
    for subtask in subtasks:
        if subtask.name == old_subtask_name:
            subtask.name = new_subtask_name
            subtask.save()
            break


def delete_subtask(task, subtask_name):
    task.subtasks.delete(name=subtask_name)


def change_subtask_status(task, subtask_name, status):
    subtasks = task.subtasks
    for subtask in subtasks:
        if subtask.name == subtask_name:
            subtask.status = status
            break


def change_deadline(task, deadline):
    task.deadline = deadline
    task.save()


def delete_deadline(task):
    task.deadline = None
    task.save()

