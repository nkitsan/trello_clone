"""
This module provides a work with a database on the server-side.
It works with essences like a calendar(collection of user events),
a habit_tracker(collection of user habits), public and weekly tasks.
It also has a possibility to work with a task which is a part of
public or private tasks

Example of use:
    from tasker.libs.managers import calendar_manager

    username = 'your username'
    event_name = 'your birthday'
    date = '29-09-2018 15:00'

    event = calendar.manager.create_event(username, event_name, date)
"""