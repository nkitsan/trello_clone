"""
This library provide JSON responses from client requests for habit
"""
from tasker.libs.managers import user_manager, public_task_manager


def get_public_tasks(api, list_id):
    username = user_manager.get_username(api)
    tasks = public_task_manager.get_list_tasks(username, list_id)
    response_tasks = {}
    if not tasks.exists():
        return {'error': 'user have no tasks in list'}
    for task in tasks:
        response_tasks[task.id] = {'name': task.task.name}
    return response_tasks


def post_public_tasks(api, list_id, task_name):
    username = user_manager.get_username(api)
    public_task = public_task_manager.create_public_task(username, list_id, task_name)
    return {public_task.id: {'name': public_task.task.name}}


def delete_public_task(api, list_id, task_id):
    username = user_manager.get_username(api)
    task = public_task_manager.get_list_task(username, list_id, task_id)
    if task is None:
        return {'error': 'this task was not found'}
    public_task_manager.delete_public_task(username, list_id, task_id)
    return {}