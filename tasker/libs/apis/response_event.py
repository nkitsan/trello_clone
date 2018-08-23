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


def delete_event(api, event_id):
    username = user_manager.get_username(api)
    event = calendar_manager.find_user_event(username, event_id)
    if event is None:
        return {'error': 'user have no event with such id'}
    calendar_manager.delete_event(username, event_id)
    return {}


def get_event(api, event_id):
    username = user_manager.get_username(api)
    event = calendar_manager.find_user_event(username, event_id)
    if event is None:
        return {'error': 'user have no event with such id'}
    response_event = {event_id: {'name': event.name, 'date': event.event_date, 'remember': {}, 'comment': {}}}
    for comment in event.comments:
        response_event[event_id]['comment'].update({comment.id:comment.comment})
    for remember in event.remember:
        response_event[event_id]['remember'].update({remember.id: remember.remember})
    return response_event


def post_event_params(api, event_id, text_comment, remember):
    username = user_manager.get_username(api)
    event = calendar_manager.find_user_event(username, event_id)
    if event is None:
        return {'error': 'user have no event with such id'}
    if text_comment is not None:
        calendar_manager.add_event_comment(username, event_id, text_comment)
    if remember is not None:
        calendar_manager.add_event_remember(username, event_id, remember)
    return get_event(api, event_id)


def put_event(api, event_id, event_name, event_date):
    username = user_manager.get_username(api)
    event = calendar_manager.find_user_event(username, event_id)
    if event is None:
        return {'error': 'user have no event with such id'}
    if event_name is not None:
        calendar_manager.change_event_name(username, event_id, event_name)
    if event_date is not None:
        calendar_manager.change_event_date(username, event_id, event_date)
    return get_event(api, event_id)


def delete_event_params(api, event_id, comment_id, remember_id):
    username = user_manager.get_username(api)
    event = calendar_manager.find_user_event(username, event_id)
    if event is None:
        return {'error': 'user have no event with such id'}
    if comment_id is not None:
        calendar_manager.delete_event_comment(username, event_id, comment_id)
    if remember_id is not None:
        calendar_manager.delete_event_remember(username, event_id, remember_id)
    return get_event(api, event_id)