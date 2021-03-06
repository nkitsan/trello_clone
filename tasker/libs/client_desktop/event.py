import requests
import click
from tasker.libs.client_desktop.helper import HOST, date_validation
from tasker.libs.client_desktop.access import read_api


@click.group()
def event_operations():
    """Here is commands which allow to work with calendar events"""


@event_operations.command(short_help='Add the event to the calendar')
@click.option('--name', default='', help='Name of the event which will be added')
@click.option('--date', required=True, help='Date of event')
def add_event(name, date):
    if not date_validation(date):
        click.echo('Format of date should be Y-M-D H:M')
        return
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    url = HOST + api + '/events'
    data = {'event_name': name, 'event_date': date}
    event_response = requests.post(url=url, data=data).json()
    if 'error' in event_response:
        click.echo(event_response['error'])
        return
    for event_id in event_response:
        click.echo(event_id + ': ' + event_response[event_id]['name'] + '\ndate: '
                   + ' '.join(event_response[event_id]['date'][0:-1].split('T')))
    return


@event_operations.command(short_help='Change the event to the calendar')
@click.option('--event_id', required=True, type=click.INT, help='ID of the event to change')
@click.option('--name', default=None, help='Name of the event on which will be renewed')
@click.option('--date', default=None, help='Date of event on which will be renewed')
def change_event(event_id, name, date):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    event_id = str(event_id)
    url = HOST + api + '/events/' + event_id
    data = {}
    if name is not None:
        data.update({'event_name': name})
    if date is not None:
        data.update({'event_date': date})
    event_response = requests.put(url=url, data=data).json()
    if 'error' in event_response:
        click.echo(event_response['error'])
        return
    click.echo(event_id + ': ' + event_response[event_id]['name'] + '\ndate: '
               + ' '.join(event_response[event_id]['date'][0:-1].split('T')))
    return


@event_operations.command(short_help='Delete the event from the calendar')
@click.option('--event_id', required=True, type=click.INT, help='ID of the event to delete')
def delete_event(event_id):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    url = HOST + api + '/events'
    data = {'event_id': str(event_id)}
    event_response = requests.delete(url=url, data=data).json()
    if 'error' in event_response:
        click.echo(event_response['error'])
        return
    click.echo('event was deleted')
    return


@event_operations.command(short_help='Show events in the calendar')
def show_events():
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    url = HOST + api + '/events'
    event_response = requests.get(url=url).json()
    if 'error' in event_response:
        click.echo(event_response['error'])
        return
    events = ''
    for event_id in event_response:
        events += (event_id + ' ' + event_response[event_id]['name'] + '\ndate:' +
                   ' '.join(event_response[event_id]['date'][0:-1].split('T')) + '\n')
    click.echo(events.rstrip('\n'))
    return


@event_operations.command(short_help='Show the event from the calendar')
@click.option('--event_id', required=True, type=click.INT, help='ID of the event to see')
def show_event(event_id):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    event_id = str(event_id)
    url = HOST + api + '/events/' + event_id
    event_response = requests.get(url=url).json()
    if 'error' in event_response:
        click.echo(event_response['error'])
        return
    click.echo(event_id + ': ' + event_response[event_id]['name'] + '\ndate: '
               + ' '.join(event_response[event_id]['date'][0:-1].split('T')))
    return
