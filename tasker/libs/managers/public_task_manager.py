"""
This manager controls server-side work with a data and responsible for changing tasks in userlists
"""


from tasker.models import User, List, PublicTask, Task
from .task_manager import *


def create_list(username, list_name):
    user = User.objects.get(username=username)
    user.lists.create(name=list_name)