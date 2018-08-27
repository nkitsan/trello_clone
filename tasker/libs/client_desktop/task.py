import requests
from .config import HOST


def add_task(api, list_id, name):
    data = {'task_name': name}
    if list_id is None:
        url = HOST + api + '/tasks'
        task_response = requests.post(url=url, data=data).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks'
        task_response = requests.post(url=url, data=data).json()
    if task_response['error'] is not None:
        return task_response['error']
    task_id = task_response.keys()[0]
    return task_id + ' ' + task_response[task_id]['name']


def change_task(api, list_id, task_id, name, status, deadline):
    data = {}
    if name is not None:
        data.update({'task_name': name})
    if status is not None and (status == 'F' or status == 'IN' or status == 'NS'):
        data.update({'task_status': status})
    if deadline is not None:
        data.update({'task_deadline': deadline})
    if list_id is None:
        url = HOST + api + '/tasks/' + str(task_id)
        task_response = requests.put(url=url, data=data).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + str(task_id)
        task_response = requests.put(url=url, data=data).json()
    if task_response['error'] is not None:
        return task_response['error']
    task_id = task_response.keys()[0]
    return task_id + ' ' + task_response[task_id]['name']


def delete_task(api, list_id, task_id):
    data = {'task_id': task_id}
    if list_id is None:
        url = HOST + api + '/tasks'
        task_response = requests.delete(url=url, data=data).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks'
        task_response = requests.delete(url=url, data=data).json()
    if task_response['error'] is not None:
        return task_response['error']
    return 'task was deleted successfully'


def show_tasks(api, list_id):
    if list_id is None:
        url = HOST + api + '/tasks'
        task_response = requests.get(url=url).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks'
        task_response = requests.get(url=url).json()
    if task_response['error'] is not None:
        return task_response['error']
    tasks = ''
    for task_id in task_response:
        tasks += task_id + ' ' + task_response[task_id]['name'] + '\n'
    return tasks


def show_task(api, list_id, task_id):
    if list_id is None:
        url = HOST + api + '/tasks/' + str(task_id)
        task_response = requests.get(url=url).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + str(task_id)
        task_response = requests.get(url=url).json()
    if task_response['error'] is not None:
        return task_response['error']
    task = (task_id + ' ' + task_response[task_id]['name'] + '\nstatus: ' + task_response[task_id]['status']
            + '\ndeadline' + task_response[task_id]['deadline'])
    if list_id is not None:
        task += '\nexecutors:'
        for executor in task_response[task_id]['executors']:
            task += ' ' + executor
    return task


