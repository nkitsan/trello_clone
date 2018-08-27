import requests
from .config import HOST


def add_habit(api, name):
    url = HOST + api + '/habits'
    data = {'habit_name': name}
    habit_response = requests.post(url=url, data=data).json()
    if habit_response['error'] is not None:
        return habit_response['error']
    habit_id = habit_response.keys()[0]
    return habit_id + ' ' + habit_response[habit_id]['name']


def change_habit(api, habit_id, name=None, status=None, timeline=None):
    url = HOST + api + '/habits/' + str(habit_id)
    data = {}
    if name is not None:
        data.update({'habit_name': name})
    if status is not None:
        data.update({'habit_status': status})
    if timeline is not None:
        data.update({'habit_timeline': timeline})
    habit_response = requests.put(url=url, data=data).json()
    if habit_response['error'] is not None:
        return habit_response['error']
    habit_info = (habit_id + habit_response[habit_id]['name'] + '\nstatus: ' + habit_response[habit_id]['status']
                  + '\ntimeline: ' + habit_response[habit_id ]['timeline'])
    return habit_info


def delete_habit(api, habit_id):
    url = HOST + api + '/habits'
    data = {'habit_id': habit_id}
    habit_response = requests.delete(url=url, data=data).json()
    if habit_response['error'] is not None:
        return habit_response['error']
    return 'habit was deleted successfully'


def show_habits(api):
    url = HOST + api + '/habits'
    habit_response = requests.get(url=url).json()
    habits = ''
    if habit_response['error'] is not None:
        return habit_response['error']
    for habit_id in habit_response:
        habits += habit_id + ' ' + habit_response[habit_id]['name'] + '\n'
    return habits


def show_habit(api, habit_id):
    url = HOST + api + '/habits/' + str(habit_id)
    habit_response = requests.get(url=url).json()
    if habit_response['error'] is not None:
        return habit_response['error']
    habit_info = (habit_id + habit_response[habit_id]['name'] + '\nstatus: ' + habit_response[habit_id]['status']
                  + '\ntimeline: ' + habit_response[habit_id]['timeline'])
    return habit_info


