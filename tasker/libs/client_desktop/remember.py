import requests
import datetime
from .config import HOST


TIME_PATTERN = '%Y-%m-%d %H:%M'


def add_remember(api, event_id, task_id, date):
    if not _date_validation(date):
        return 'wrong datetime format'
    data = {'remember': date}
    if event_id is not None:
        url = HOST + api + '/events/' + str(event_id)
        response_remember = requests.post(url=url, data=data).json()
    else:
        url = HOST + api + '/tasks/' + str(task_id)
        response_remember = requests.post(url=url, data=data).json()
    if response_remember['error'] is not None:
        return response_remember['error']
    return 'remember was successfully added'


def delete_remember(api, event_id, task_id, remember_id):
    data = {'remember_id': remember_id}
    if event_id is not None:
        url = HOST + api + '/events/' + str(event_id)
        response_remember = requests.delete(url=url, data=data).json()
    else:
        url = HOST + api + '/tasks/' + str(task_id)
        response_remember = requests.delete(url=url, data=data).json()
    if response_remember['error'] is not None:
        return response_remember['error']
    return 'remember was successfully deleted'


def show_remembers(api, event_id, task_id):
    remembers = []
    if event_id is not None:
        url = HOST + api + '/events/' + str(event_id)
        response_remember = requests.get(url=url).json()
        if response_remember['error'] is None:
            remembers = response_remember[event_id]['remember']
    else:
        url = HOST + api + '/tasks/' + str(task_id)
        response_remember = requests.get(url=url).json()
        if response_remember['error'] is None:
            remembers = response_remember[task_id]['remember']
    if response_remember['error'] is not None:
        return response_remember['error']
    result = ''
    for remember_id in remembers:
        result += remember_id + ': ' + remembers[remember_id]
    return result


def _date_validation(date):
    try:
        datetime.datetime.strptime(date, TIME_PATTERN)
    except ValueError:
        return False
    return True
