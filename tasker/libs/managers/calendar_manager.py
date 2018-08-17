"""
Manager for adding, deleting and changing events in the calendar
"""


from tasker.models import User, Calender, Event
from .task_manager import *


def create_event(username, event_name, event_date):
    user = User.objects.get(username=username)
    user.calendar.events.create(name=event_name, event_date=event_date)


def delete_event(username, event_name):
    user = User.objects.get(username=username)
    user.calendar.events.delete(name=event_name)


def change_event_name(username, event_name, new_event_name):
    user = User.objects.get(username=username)
    event = user.calendar.events.get(event_name=event_name)
    event.name = new_event_name
    event.save()


def change_event_date(username, event_name, new_event_date):
    user = User.objects.get(username=username)
    event = user.calendar.events.get(event_name=event_name)
    event.event_date = new_event_date
    event.save()


def add_event_comment(username, event_name, comment):
    user = User.objects.get(username=username)
    event = user.calendar.events.get(event_name=event_name)
    event.comments.create(comment=comment)


def delete_event_comment(username, event_name, comment):
    user = User.objects.get(username=username)
    event = user.calendar.events.get(event_name=event_name)
    event.comments.delete(comment=comment)


def add_event_remember(username, event_name, remember):
    user = User.objects.get(username=username)
    event = user.calendar.events.get(event_name=event_name)
    event.remember.create(repeate_date=remember)


def delete_event_remember(username, event_name, remember):
    user = User.objects.get(username=username)
    event = user.calendar.events.get(event_name=event_name)
    event.remember.delete(repeate_date=remember)



