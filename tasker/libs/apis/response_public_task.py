"""
This library provide JSON responses from client requests for habit
"""
from tasker.libs.managers import user_manager, public_task_manager


def get_public_tasks(api, list_id):
    username = user_manager.get_username(api)
    tasks = public_task_manager.get_list_tasks(username, list_id)
    response_tasks = {}
    if tasks is None:
        return {'error': 'user have no lists'}
    for task in tasks:
        response_tasks[task.id] = {'name': task.id}
    return response_tasks


def post_public_tasks(api, list_id, task_name):
    username = user_manager.get_username(api)
    public_task = public_task_manager.create_public_task(username, list_id, task_name)
    return {public_task.id: {'name': public_task.name}}