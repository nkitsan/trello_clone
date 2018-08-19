"""
Manager for adding, deleting and changing events in the calendar
"""


from tasker.models import User, Event


def create_event(username, event_name, event_date):
    user = User.objects.get(username=username)
    user.calendar.create(name=event_name, event_date=event_date)


def delete_event(username, event_id):
    user = User.objects.get(username=username)
    user.calendar.delete(id=event_id)


def change_event_name(username, event_id, new_event_name):
    event = find_user_event(username, event_id)
    event.name = new_event_name
    event.save()


def change_event_date(username, event_id, new_event_date):
    event = find_user_event(username, event_id)
    event.event_date = new_event_date
    event.save()


def add_event_comment(username, event_id, comment):
    event = find_user_event(username, event_id)
    event.comments.create(comment=comment)


def delete_event_comment(username, event_id, comment_id):
    event = find_user_event(username, event_id)
    event.comments.delete(id=comment_id)


def add_event_remember(username, event_id, remember):
    event = find_user_event(username, event_id)
    event.remember.create(repeate_date=remember)


def delete_event_remember(username, event_id, remember_id):
    event = find_user_event(username, event_id)
    event.remember.delete(id=remember_id)


def find_user_event(username, event_id):
    user = User.objects.get(username=username)
    return user.calendar.get(id=event_id)


