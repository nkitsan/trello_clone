"""
This library provide JSON responses from client requests for habit
"""
from tasker.libs.managers import user_manager, public_task_manager


def get_lists(api):
    username = user_manager.get_username(api)
    lists = public_task_manager.get_user_lists(username)
    response_lists = {}
    if not lists.exists():
        return {'error': 'user have no lists'}
    for public_list in lists:
        response_lists[public_list.id] = {'name': public_list.name}
    return response_lists


def post_lists(api, list_name):
    username = user_manager.get_username(api)
    public_list = public_task_manager.create_public_list(username, list_name)
    return {public_list.id: {'name': public_list.name}}