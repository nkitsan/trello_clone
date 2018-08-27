import requests
from .config import HOST


def add_user(api, list_id, task_id, username):
    if task_id is None:
        url = HOST + api + '/lists/' + str(list_id)
        data = {'new_user': username}
        response = requests.post(url=url, data=data).json()
        if response['error'] is None:
            return 'list was added successfully to user lists'
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + str(task_id)
        data = {'executor': username}
        response = requests.post(url=url, data=data).json()
    if response['error'] is not None:
        return response['error']
    return 'executor was successfully added'


def delete_user(api, list_id, task_id, username):
    if task_id is None:
        url = HOST + api + '/lists/' + str(list_id)
        data = {'new_user': username}
        response = requests.delete(url=url, data=data).json()
        if response['error'] is None:
            return 'list was deleted successfully from user lists'
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + str(task_id)
        data = {'executor': username}
        response = requests.delete(url=url, data=data).json()
    if response['error'] is not None:
        return response['error']
    return 'executor was successfully deleted'
