"""
This module provides functions which make a new essence
based on data that parsed from client requests

Commands package provides responses
    event.py, habit.py, list.py,
    private_task.py, public_task.py


Example of use:
    from tasker.libs.apis import event
    api = 'some api key'
    events = event.get_events(api)
    name = 'new event'
    date = '19.09.2018'
    new_event = event.post_event(api, name, date)
"""