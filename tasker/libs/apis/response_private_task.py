"""
This library provide JSON responses from client requests for habit
"""
from tasker.libs.managers import user_manager, weekly_task_manager


def get_tasks(api):
    username = user_manager.get_username(api)
    tasks = weekly_task_manager.get_weekly_tasks(username)
    response_tasks = {}
    if not tasks.exists():
        return {'error': 'user have no weekly tasks'}
    for task in tasks:
        response_tasks[task.id] = {'name': task.task.name}
    return response_tasks


def post_task(api, task_name):
    username = user_manager.get_username(api)
    task = weekly_task_manager.add_weeklytask(username, task_name)
    return {task.id: {'name': task.task.name}}


def delete_task(api, task_id):
    username = user_manager.get_username(api)
    task = weekly_task_manager.find_user_task(username, task_id)
    if task is None:
        return {'error': 'user does not have the task in weeklytasks'}
    weekly_task_manager.delete_weeklytask(username, task_id)