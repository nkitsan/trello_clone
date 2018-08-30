import click
from tasker.libs.client_desktop.task import task_operations
from tasker.libs.client_desktop.subtask import subtask_operations
from tasker.libs.client_desktop.repeat import repeat_operations
from tasker.libs.client_desktop.remember import remember_operations
from tasker.libs.client_desktop.list import list_operations
from tasker.libs.client_desktop.habit import habit_operations
from tasker.libs.client_desktop.comment import comment_operations
from tasker.libs.client_desktop.access import access_operations
from tasker.libs.client_desktop.event import event_operations


tasker = click.CommandCollection(sources=[task_operations,  habit_operations, subtask_operations, repeat_operations,
                                          remember_operations, list_operations, habit_operations, comment_operations,
                                          access_operations, event_operations])


def cli():
    tasker()
