"""
This module provides cli decorators which interacts with
server api and print returns in a easy-to-read format.

It can be used to make a new command-line programs with
simplified functionality like a calendar, a habit tracker
or a tracker for tasks.

Example:
    -install click tool
    -create new file main.py
    -type in it main.py:

    import click
    from tasker.libs.client_desktop.event import event_operations
    from tasker.libs.client_desktop.access import access_operations

    tasker = click.CommandCollection(sources=[event_operations, access_operations])

    def cli():
        tasker()


    - now you can run main.py in folder with it and use a calendar
"""