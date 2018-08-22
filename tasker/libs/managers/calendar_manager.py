"""
Manager for adding, deleting and changing events in the calendar
"""


from tasker.models import User, Event


def create_event(username, event_name, event_date):
    user = User.objects.get(username=username)
    user.calendar.create(name=event_name, event_date=event_date)


def delete_event(username, event_id):
    user = User.objects.get(username=username)
    user.calendar.filter(id=event_id).delete()


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
    return event.comments.create(comment=comment)


def delete_event_comment(username, event_id, comment_id):
    event = find_user_event(username, event_id)
    event.comments.filter(id=comment_id).delete()


def add_event_remember(username, event_id, remember):
    event = find_user_event(username, event_id)
    return event.remember.create(repeat_date=remember)


def delete_event_remember(username, event_id, remember_id):
    event = find_user_event(username, event_id)
    event.remember.filter(id=remember_id).delete()


def find_user_event(username, event_id):
    user = User.objects.get(username=username)
    if user.calendar.filter(id=event_id).exists():
        return user.calendar.get(id=event_id)
    else:
        return None


def get_events(username):
    user = User.objects.get(username=username)
    return user.calendar.all()