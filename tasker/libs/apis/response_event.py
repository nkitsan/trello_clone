"""
This library provide JSON responses from client requests for habit
"""
from tasker.libs.managers import user_manager, calendar_manager


def get_events(api):
    username = user_manager.get_username(api)
    events = calendar_manager.get_events(username)
    response_event = {}
    if not events.exists():
        return {'error': 'user have no events'}
    for event in events:
        response_event[event.id] = {'name': event.name, 'date': event.event_date}
    return response_event


def post_event(api, event_name, event_date):
    username = user_manager.get_username(api)
    event = calendar_manager.create_event(username, event_name, event_date)
    return {event.id: {'name': event.name, 'date': event.event_date}}