import requests
from .config import host


def add_event(api, name, date):
    url = host + api + '/events'
    data = {'event_name': name, 'event_date': date}
    event_response = requests.post(url=url, data=data).json()
    if event_response['error'] is not None:
        return event_response['error']
    event_id = event_response.keys()[0]
    return event_id + ' ' + event_response[event_id]['name'] + '\n' +event_response[event_id]['date']


def change_event(api, event_id, name, date):
    url = host + api + '/events/' + str(event_id)
    data = {}
    if name is not None:
        data.update({'event_name': name})
    if date is not None:
        data.update({'event_date': date})
    event_response = requests.put(url=url, data=data).json()
    if event_response['error'] is not None:
        return event_response['error']
    return event_id + ' ' + event_response[event_id]['name'] + '\n' + event_response[event_id]['date']


def delete_event(api, event_id):
    url = host + api + '/events'
    data = {'event_id': event_id}
    event_response = requests.delete(url=url, data=data).json()
    if event_response['error'] is not None:
        return event_response['error']
    return 'event was deleted '


def show_events(api):
    url = host + api + '/events'
    event_response = requests.get(url=url).json()
    if event_response['error'] is not None:
        return event_response['error']
    events = ''
    for event_id in event_response:
        events += event_id + ' ' + event_response[event_id]['name'] + '\n' + event_response[event_id]['date'] + '\n'
    return events


def show_event(api, event_id):
    url = host + api + '/events/' + str(event_id)
    event_response = requests.get(url=url).json()
    if event_response['error'] is not None:
        return event_response['error']
    return event_id + ' ' + event_response[event_id]['name'] + '\n' + event_response[event_id]['date']

