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


def delete_list(api, list_id):
    username = user_manager.get_username(api)
    lists = public_task_manager.get_user_lists(username)
    if not lists.filter(id=list_id).exists():
        return {'error': 'no such list'}
    public_task_manager.delete_public_list(username, list_id)
    return {}


def post_list_params(api, list_id, new_user):
    username = user_manager.get_username(api)
    user = user_manager.get_user(username)
    if not user.lists.filter(id=list_id).exists():
        return {'error': 'no access to manage this list'}
    public_task_manager.add_public_list_user(username, new_user, list_id)


def put_list(api, list_id, list_name):
    username = user_manager.get_username(api)
    public_task_manager.change_public_list_name(username, list_id, list_name)
    return {list_id: list_name}


def delete_list_params(api, list_id, new_user):
    username = user_manager.get_username(api)
    user = user_manager.get_user(username)
    if not user.lists.filter(id=list_id).exists():
        return {'error': 'no access to manage this list'}
    public_task_manager.delete_public_list_user(username, new_user, list_id)
    return {}
