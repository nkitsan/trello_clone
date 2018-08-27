import requests
from .config import host


def add_repeat(api, task_id, repeat):
    if repeat > 6 or repeat < 0:
        return 'wrong repeat format'
    data = {'repeat': repeat}
    url = host + api + '/tasks/' + str(task_id)
    response_repeat = requests.post(url=url, data=data).json()
    if response_repeat['error'] is not None:
        return response_repeat['error']
    return 'repeat was successfully added'


def delete_repeat(api, task_id, repeat_id):
    data = {'repeat_id': repeat_id}
    url = host + api + '/tasks/' + str(task_id)
    response_repeat = requests.delete(url=url, data=data).json()
    if response_repeat['error'] is not None:
        return response_repeat['error']
    return 'repeat was successfully deleted'


def show_repeats(api, event_id, task_id):
    url = host + api + '/tasks/' + str(task_id)
    response_repeat = requests.get(url=url).json()
    if response_repeat['error'] is not None:
        return response_repeat['error']
    result = ''
    for repeat_id in response_repeat[task_id]['']:
        result += remember_id + ': ' + remembers[remember_id]
    return result


def _date_validation(date):
    try:
        datetime.datetime.strptime(date, time_pattern)
    except ValueError:
        return False
    return True
