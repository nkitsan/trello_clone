import requests
from .config import HOST


def add_list(api, name):
    data = {'list_name': name}
    url = HOST + api + '/lists'
    list_response = requests.post(url=url, data=data).json()
    list_id = list_response.keys()[0]
    if list_response['error'] is not None:
        return list_response['error']
    return list_id + list_response[list_id]['name']


def change_list(api, list_id, name):
    data = {'list_name': name}
    url = HOST + api + '/lists/' + str(list_id)
    list_response = requests.put(url=url, data=data).json()
    if list_response['error'] is not None:
        return list_response['error']
    return list_id + list_response[list_id]['name']


def delete_list(api, list_id):
    data = {'list_id': list_id}
    url = HOST + api + '/lists'
    list_response = requests.delete(url=url, data=data).json()
    if list_response['error'] is not None:
        return list_response['error']
    return 'list was deleted successfully'


def show_lists(api):
    url = HOST + api + '/lists'
    list_response = requests.get(url=url).json()
    if list_response['error'] is not None:
        return list_response['error']
    lists = ''
    for list_id in list_response:
        lists += list_id + list_response[list_id]['name'] + '\n'
    return lists