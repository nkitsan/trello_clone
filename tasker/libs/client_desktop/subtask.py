import requests
from .config import host


def add_subtask(api, list_id, task_id, subtask):
    data = {'subtask': subtask}
    if list_id is None:
        url = host + api + '/tasks/' + str(task_id)
        response_subtask = requests.post(url=url, data=data).json()
    else:
        url = host + api + '/lists/' + list_id + '/tasks/' + str(task_id)
        response_subtask = requests.post(url=url, data=data).json()
    if response_subtask['error'] is not None:
        return response_subtask['error']
    return 'subtask was successfully added'


def delete_subtask(api, list_id, task_id, subtask_id):
    data = {'subtask_id': subtask_id}
    if list_id is None:
        url = host + api + '/tasks/' + str(task_id)
        response_subtask = requests.delete(url=url, data=data).json()
    else:
        url = host + api + '/lists/' + list_id + '/tasks/' + str(task_id)
        response_subtask = requests.delete(url=url, data=data).json()
    if response_subtask['error'] is not None:
        return response_subtask['error']
    return 'subtask was successfully deleted'


def change_subtask_status(api, list_id, task_id, subtask_id, status):
    if status == 'NS' or status == 'F':
        data = {'subtask_id': subtask_id, 'subtask_status': status}
    else:
        return 'Incorrect value of status'
    if list_id is None:
        url = host + api + '/tasks/' + str(task_id)
        response_subtask = requests.put(url=url, data=data).json()
    else:
        url = host + api + '/lists/' + list_id + '/tasks/' + str(task_id)
        response_subtask = requests.put(url=url, data=data).json()
    if response_subtask['error'] is not None:
        return response_subtask['error']
    return 'subtask status was successfully changed'


def show_subtasks(api, list_id, task_id):
    if list_id is None:
        url = host + api + '/tasks/' + str(task_id)
        response_subtask = requests.get(url=url).json()
    else:
        url = host + api + '/lists/' + list_id + '/tasks/' + str(task_id)
        response_subtask = requests.get(url=url).json()
    if response_subtask['error'] is not None:
        return response_subtask['error']
    subtasks = response_subtask[task_id]['subtasks']
    result = ''
    for subtask_id in subtasks:
        result += (subtask_id + ': ' + subtasks[subtask_id]['name'] + '\nstatus: ' + subtasks[subtask_id]['status']
                   + '\n')