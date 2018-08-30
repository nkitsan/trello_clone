import requests
import click
from .helper import HOST, date_validation, api


@click.group()
def remember_operations():
    """Here is commands which you can use to manipulate with remember of tasks in private (weekly task) list
    and remembers in events"""


@remember_operations.command(short_help='Create a new remember for a task or an event')
@click.option('--event_id', default=None, type=click.INT,
              help='ID of the event to add a remember')
@click.option('--task_id', default=None, type=click.INT,
              help='ID of the task to add a remember')
@click.option('--remember', default=None, help='Remeber of the task or the event')
def add_remember(event_id, task_id, remember):
    if remember is None:
        click.echo('You forget to enter date to remember')
        return
    if event_id is None and task_id is None:
        click.echo('You forget to add a task or an event id to add a remember')
        return
    if not date_validation(remember):
        click.echo('wrong datetime format')
        return
    data = {'remember': remember}
    if event_id is not None:
        url = HOST + api + '/events/' + str(event_id)
        response_remember = requests.post(url=url, data=data).json()
    else:
        url = HOST + api + '/tasks/' + str(task_id)
        response_remember = requests.post(url=url, data=data).json()
    if 'error' in response_remember:
        click.echo(response_remember['error'])
        return
    click.echo('remember was successfully added')


@remember_operations.command(short_help='Delete a remember for a task or an event')
@click.option('--event_id', default=None, type=click.INT,
              help='ID of the event to delete the remember')
@click.option('--task_id', default=None, type=click.INT,
              help='ID of the task to delete the remember')
@click.option('--remember_id', default=None, help='Remeber ID of the task or the event')
def delete_remember(event_id, task_id, remember_id):
    if event_id is None and task_id is None:
        click.echo('You forget to add a task or an event id to delete the remember')
        return
    data = {'remember_id': str(remember_id)}
    if event_id is not None:
        url = HOST + api + '/events/' + str(event_id)
        response_remember = requests.delete(url=url, data=data).json()
    else:
        url = HOST + api + '/tasks/' + str(task_id)
        response_remember = requests.delete(url=url, data=data).json()
    if 'error' in response_remember:
        click.echo(response_remember['error'])
        return
    click.echo('remember was successfully deleted')
    return


@remember_operations.command(short_help='Show remembers for a task or an event')
@click.option('--event_id', default=None, type=click.INT,
              help='ID of the event to show its remembers')
@click.option('--task_id', default=None, type=click.INT,
              help='ID of the task to show the remembers')
def show_remembers(event_id, task_id):
    if event_id is None and task_id is None:
        click.echo('You forget to add a task or an event id to delete the remember')
        return
    remembers = []
    if event_id is not None:
        event_id = str(event_id)
        url = HOST + api + '/events/' + event_id
        response_remember = requests.get(url=url).json()
        if 'error' not in response_remember:
            remembers = response_remember[event_id]['remembers']
    else:
        task_id = str(task_id)
        url = HOST + api + '/tasks/' + task_id
        response_remember = requests.get(url=url).json()
        if 'error' not in response_remember:
            remembers = response_remember[task_id]['remembers']
    if 'error' in response_remember:
        click.echo(response_remember['error'])
        return
    result = ''
    for remember_id in remembers:
        result += remember_id + ': ' + ' '.join(remembers[remember_id][:-1].split('T')) + '\n'
    if result == '':
        click.echo('No remembers here :(')
        return
    click.echo(result.rstrip('\n'))
    return
