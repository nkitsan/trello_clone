"""
This code provide responses in a dict format
for client requests about events
"""
from tasker.libs.managers import user_manager, calendar_manager
import datetime


class Event:

    def __init__(self, api):
        self.api = api

    def get_events(self):
        """
        Returns all events of user with provided api-key in the format
        {id_1: {'name': name_1, 'date': date_1}, id_2: {'name': name_2, 'date': date_2}...}
        """
        username = user_manager.get_username(self.api)
        events = calendar_manager.get_events(username)
        response_event = {}
        if not events.exists():
            return {'error': 'user have no events'}
        for event in events:
            response_event[event.id] = {'name': event.name, 'date': event.event_date}
        return response_event

    def post_event(self, event_name, event_date):
        """
        Create new event with name - event_name and to the date
        - event_date and returns a new event in the format
        {id_1: {'name': name_1, 'date': date_1}}
        """
        username = user_manager.get_username(self.api)
        event = calendar_manager.create_event(username, event_name, event_date)
        return {event.id: {'name': event.name, 'date': event.event_date}}

    def delete_event(self, event_id):
        """
        Deletes the user event with provided event_id
        and returns empty dict
        """
        username = user_manager.get_username(self.api)
        event = calendar_manager.find_user_event(username, event_id)
        if event is None:
            return {'error': 'user have no event with such id'}
        calendar_manager.delete_event(username, event_id)
        return {}

    def get_event(self, event_id):
        """Returns the event full info such as name, date, remembers and comments"""
        username = user_manager.get_username(self.api)
        event = calendar_manager.find_user_event(username, event_id)
        if event is None:
            return {'error': 'user have no event with such id'}
        response_event = {event_id: {'name': event.name, 'date': event.event_date, 'remembers': {}, 'comments': {}}}
        for comment in event.comments.all():
            response_event[event_id]['comments'].update({comment.id: comment.comment})
        for remember in event.remember.all():
            response_event[event_id]['remembers'].update({remember.id: remember.repeat_date})
        return response_event

    def post_event_params(self, event_id, text_comment, remember):
        """
        Adds a new comment and/or remember to event and
        returns a full info about event
        """
        username = user_manager.get_username(self.api)
        event = calendar_manager.find_user_event(username, event_id)
        if event is None:
            return {'error': 'user have no event with such id'}
        if text_comment is not None:
            calendar_manager.add_event_comment(username, event_id, text_comment)
        if remember is not None:
            calendar_manager.add_event_remember(username, event_id, remember)
        return self.get_event(event_id)

    def put_event(self, event_id, event_name, event_date):
        """
        Changes event name and/or date and
        returns modified event in the full format
        """
        username = user_manager.get_username(self.api)
        event = calendar_manager.find_user_event(username, event_id)
        if event is None:
            return {'error': 'user have no event with such id'}
        if event_name is not None:
            calendar_manager.change_event_name(username, event_id, event_name)
        if event_date is not None:
            calendar_manager.change_event_date(username, event_id, event_date)
        return self.get_event(event_id)

    def delete_event_params(self, event_id, comment_id, remember_id):
        """
        Deletes the remember and/or the comment of the event
        and returns a modified event in the full format
        """
        username = user_manager.get_username(self.api)
        event = calendar_manager.find_user_event(username, event_id)
        if event is None:
            return {'error': 'user have no event with such id'}
        if comment_id is not None:
            calendar_manager.delete_event_comment(username, event_id, comment_id)
        if remember_id is not None:
            calendar_manager.delete_event_remember(username, event_id, remember_id)
        return self.get_event(event_id)

    def check_remembers(self):
        """
        Makes a dictionary with remembers which should be shown
        to users and returns it in the format
        {id_1: {'name': name_1, 'remember': remember_1},
        id_2: {'name': name_2, 'remember': remember_2}}
        """
        username = user_manager.get_username(self.api)
        events = calendar_manager.get_events(username)
        events_response = {}
        for event in events:
            for remember in event.remember.all():
                if remember.repeat_date <= datetime.datetime.now(datetime.timezone.utc):
                    events_response.update({remember.id: {'name': event.name,
                                                          'event_id': event.id,
                                                          'remember': remember.repeat_date}})
        return events_response
