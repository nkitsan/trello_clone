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
    return {}


def get_task(api, task_id):
    username = user_manager.get_username(api)
    task = weekly_task_manager.find_user_task(username, task_id)
    if task is None:
        return {'error': 'user does not have the task in weeklytasks'}
    response_task = {task.id: {'name': task.task.name, 'status': task.task.status, 'deadline': task.task.deadline,
                               'comments': {}, 'subtasks': {}, 'remember': {}, 'repeat': {}}}
    for comment in task.task.comments.all():
        response_task[task.id]['comments'].update({comment.id: comment.comment})
    for subtask in task.task.subtasks.all():
        response_task[task.id]['subtasks'].update({subtask.id: {'name': subtask.name, 'status': subtask.status}})
    for remember in task.remember.all():
        response_task[task.id]['remember'].update({remember.id: remember.repeat_date})
    for repeat in task.repeat.all():
        response_task[task.id]['repeat'].update({repeat.id: repeat.repeat})
    return response_task


def post_task_params(api, task_id, repeat, remember, subtask, comment):
    username = user_manager.get_username(api)
    task = weekly_task_manager.find_user_task(username, task_id)
    if task is None:
        return {'error': 'user does not have the task in weeklytasks'}
    if repeat is not None:
        weekly_task_manager.add_weeklytask_repeat(username, task_id, repeat)
    if remember is not None:
        weekly_task_manager.add_weeklytask_remember(username, task_id, remember)
    if subtask is not None:
        weekly_task_manager.add_weeklytask_subtask(username, task_id, subtask)
    if comment is not None:
        weekly_task_manager.add_weeklytask_comment(username, task_id, comment)
    return get_task(api, task_id)


def put_task(api, task_id, name, status, deadline, subtask_id, subtask_status):
    username = user_manager.get_username(api)
    task = weekly_task_manager.find_user_task(username, task_id)
    if task is None:
        return {'error': 'user does not have the task in weeklytasks'}
    if name is not None:
        weekly_task_manager.change_weeklytask_name(username, task_id, name)
    if status is not None:
        weekly_task_manager.change_weeklytask_status(username, task_id, status)
    if deadline is not None:
        weekly_task_manager.change_weeklytask_deadline(username, task_id, deadline)
    if subtask_id is not None and task.task.subtasks.filter(id=subtask_id).exists():
        weekly_task_manager.change_weeklytask_subtask_status(username, task_id, subtask_id, subtask_status)
    return get_task(api, task_id)


def delete_task_params(api, task_id, comment_id, subtask_id, repeat_id, remember_id):
    username = user_manager.get_username(api)
    task = weekly_task_manager.find_user_task(username, task_id)
    if task is None:
        return {'error': 'user does not have the task in weeklytasks'}
    if comment_id is not None:
        weekly_task_manager.delete_weeklytask_comment(username, task_id, comment_id)
    if subtask_id is not None:
        weekly_task_manager.delete_weeklytask_subtask(username, task_id, subtask_id)
    if repeat_id is not None:
        weekly_task_manager.delete_weeklytask_repeat(username, task_id, repeat_id)
    if remember_id is not None:
        weekly_task_manager.delete_weeklytask_remember(username, task_id, remember_id)
    return get_task(api, task_id)