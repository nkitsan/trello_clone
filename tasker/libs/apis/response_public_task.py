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


def get_public_task(api, list_id, task_id):
    username = user_manager.get_username(api)
    task = public_task_manager.get_list_task(username, list_id, task_id)
    if task is None:
        return {'error': 'this task was not found'}
    response_task = {task.id: {'name': task.task.name, 'status': task.task.status, 'deadline': task.task.deadline,
                               'comments': {}, 'subtasks': {}, 'executors': []}}
    for comment in task.task.comments:
        response_task[task.id]['comments'].update({comment.id: comment.comment})
    for subtask in task.task.subtasks:
        response_task[task.id]['subtasks'].update({subtask.id: {'name': subtask.name, 'status': subtask.status}})
    for executor in task.executors:
        response_task[task.id]['executors'].append(executor.username)
    return response_task


def post_public_task_params(api, list_id, task_id, comment, subtask, executor):
    username = user_manager.get_username(api)
    task = public_task_manager.get_list_task(username, list_id, task_id)
    if task is None:
        return {'error': 'this task was not found'}
    if comment is not None:
        public_task_manager.add_public_task_comment(username, list_id, task_id, comment)
    if subtask is not None:
        public_task_manager.add_public_task_subtask(username, list_id, task_id, subtask)
    if executor is not None:
        public_task_manager.add_task_executor(username, executor, list_id, task_id)
    return get_public_task(api, list_id, task_id)


def put_public_task(api, list_id, task_id, name, status, deadline, subtask_id, subtask_status):
    username = user_manager.get_username(api)
    task = public_task_manager.get_list_task(username, list_id, task_id)
    if task is None:
        return {'error': 'this task was not found'}
    if name is not None:
        public_task_manager.change_public_task_name(username, list_id, task_id, name)
    if status is not None:
        public_task_manager.change_public_task_status(username, list_id, task_id, status)
    if deadline is not None:
        public_task_manager.change_public_task_deadline(username, list_id, task_id, deadline)
    if subtask_id is not None:
        public_task_manager.change_public_task_subtask_status(username, list_id, task_id, subtask_id, subtask_status)
    return get_public_task(api, list_id, task_id)


def delete_public_task_params(api, list_id, task_id, comment_id, subtask_id, executor):
    username = user_manager.get_username(api)
    task = public_task_manager.get_list_task(username, list_id, task_id)
    if task is None:
        return {'error': 'this task was not found'}
    if comment_id is not None:
        public_task_manager.delete_public_task_comment(username, list_id, task_id, comment_id)
    if subtask_id is not None:
        public_task_manager.delete_public_task_subtask(username, list_id, task_id, subtask_id)
    if executor is not None:
        public_task_manager.delete_task_executor(username, executor, list_id, task_id)
    return get_public_task(api, list_id, task_id)