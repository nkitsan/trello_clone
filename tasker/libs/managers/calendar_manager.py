"""
Manager for adding, deleting and changing events in the calendar
"""


from tasker.models import User
from tasker.libs.logger.logger import get_logs


@get_logs
def create_event(username, event_name, event_date):
    """
    Creates an event

    :param username: username of an user
    :param event_name: a name of event to create
    :param event_date: a date of event to create
    :return: essence of a created event
    """
    user = User.objects.get(username=username)
    return user.calendar.create(name=event_name, event_date=event_date)


@get_logs
def delete_event(username, event_id):
    """
    Deletes an event

    :param username: username of an user
    :param event_id: an id of the deleting event
    """
    user = User.objects.get(username=username)
    user.calendar.filter(id=event_id).delete()


@get_logs
def change_event_name(username, event_id, new_event_name):
    """
    Changes an event name

    :param username: username of an user
    :param event_id: an id of a changing event
    :param new_event_name: new name for event
    """
    event = find_user_event(username, event_id)
    event.name = new_event_name
    event.save()


@get_logs
def change_event_date(username, event_id, new_event_date):
    """
    Changes an event name

    :param username: username of an user
    :param event_id: an id of a changing event
    :param new_event_date: a new date for an event
    """
    event = find_user_event(username, event_id)
    event.event_date = new_event_date
    event.save()


@get_logs
def add_event_comment(username, event_id, comment):
    """
    Adds an comment to the event

    :param username: username of an user
    :param event_id: an id of a modifying event
    :param comment: text of a creating comment
    :return: a new essence of a comment
    """
    event = find_user_event(username, event_id)
    return event.comments.create(comment=comment)


@get_logs
def delete_event_comment(username, event_id, comment_id):
    """
    Deletes a comment in an event

    :param username: username of an user
    :param event_id: an id of an event with a comment to delete
    :param comment_id: an id of a comment to delete
    """
    event = find_user_event(username, event_id)
    event.comments.filter(id=comment_id).delete()


@get_logs
def add_event_remember(username, event_id, remember):
    """
    Creates a remember for an event

    :param username: username of an user
    :param event_id: an id of an event to add a remember
    :param remember: a date of the remember
    :return: a new essence of remember
    """
    event = find_user_event(username, event_id)
    return event.remember.create(repeat_date=remember)


@get_logs
def delete_event_remember(username, event_id, remember_id):
    """
    Deletes a remember from an event

    :param username: username of an user
    :param event_id: an id of an event with a remember to delete
    :param remember_id: an id of a remember to delete
    """
    event = find_user_event(username, event_id)
    event.remember.filter(id=remember_id).delete()


@get_logs
def find_user_event(username, event_id):
    """
    Searches an event with defined id

    :param username: username of an user
    :param event_id: : an id of a searched event
    :return: an essence of a searched event or None if event was not found
    """
    user = User.objects.get(username=username)
    if user.calendar.filter(id=event_id).exists():
        return user.calendar.get(id=event_id)
    else:
        return None


@get_logs
def get_events(username):
    """
    Returns all user events

    :param username: username of an user
    :return: array of events
    """
    user = User.objects.get(username=username)
    return user.calendar.all()