"""
This library provide JSON responses from client requests for habit
"""
from tasker.libs.managers import user_manager, weekly_task_manager


def get_tasks(api):
    username = user_manager.get_username(api)
    tasks = weekly_task_manager.get_weekly_tasks(username)
    response_tasks = {}
    if tasks is None:
        return {'error': 'user have no events'}
    for task in tasks:
        response_tasks[task.id] = {'name': task.name}
    return response_tasks


def post_task(api, task_name):
    username = user_manager.get_username(api)
    task = weekly_task_manager.add_weeklytask(username, task_name)
    return {task.id: {'name': task.name}}