import requests
import click
from .helper import HOST
from .access import read_api


@click.group()
def habit_operations():
    """Here is commands which you can use to manipulate with habits(actions which should repeat daily)"""


@habit_operations.command(short_help='Create a new habit')
@click.option('--name', default='', help='Name of a created habit')
def add_habit(name):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    url = HOST + api + '/habits'
    data = {'habit_name': name}
    habit_response = requests.post(url=url, data=data).json()
    if 'error' in habit_response:
        click.echo(habit_response['error'])
        return
    habit_id = ''
    for key in habit_response:
        habit_id = key
    click.echo(habit_id + ' ' + habit_response[habit_id]['name'])
    return


@habit_operations.command(short_help='Change the habit')
@click.option('--habit_id', default=None, type=click.INT, help='ID of habit which you want to change')
@click.option('--name', default=None, help='New name of the habit')
@click.option('--status', default=None, type=click.Choice(['NS', 'F']), help='New status of the habit')
@click.option('--timeline', default=None, type=click.IntRange(1, 500), help='New timeline of the habit')
def change_habit(habit_id, name, status, timeline):
    if habit_id is None:
        click.echo('Sorry, i am not so smart to predict which habit you want to change')
        return
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    habit_id = str(habit_id)
    url = HOST + api + '/habits/' + habit_id
    data = {}
    if name is not None:
        data.update({'habit_name': name})
    if status is not None:
        data.update({'habit_status': status})
    if timeline is not None:
        data.update({'habit_timeline': str(timeline)})
    habit_response = requests.put(url=url, data=data).json()
    if 'error' in habit_response:
        click.echo(habit_response['error'])
        return
    habit_info = (habit_id + habit_response[habit_id]['name'] + '\nstatus: ' + habit_response[habit_id]['status']
                  + '\ntimeline: ' + habit_response[habit_id ]['timeline'])
    click.echo(habit_info)
    return


@habit_operations.command(short_help='Change the habit')
@click.option('--habit_id', default=None, type=click.INT, help='ID of habit which you want to delete')
def delete_habit(habit_id):
    if habit_id is None:
        click.echo('Sorry, i am not so smart to predict which habit you want to delete')
        return
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    url = HOST + api + '/habits'
    data = {'habit_id': str(habit_id)}
    habit_response = requests.delete(url=url, data=data).json()
    if 'error' in habit_response:
        click.echo(habit_response['error'])
        return
    click.echo('habit was deleted successfully')
    return


@habit_operations.command(short_help='Show habits')
def show_habits():
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    url = HOST + api + '/habits'
    habit_response = requests.get(url=url).json()
    habits = ''
    if 'error' in habit_response:
        click.echo(habit_response['error'])
        return
    for habit_id in habit_response:
        habits += habit_id + ' ' + habit_response[habit_id]['name'] + '\n'
    click.echo(habits.rstrip('\n'))
    return


@habit_operations.command(short_help='Show the habit')
@click.option('--habit_id', default=None, type=click.INT, help='ID of habit which you want to see')
def show_habit(habit_id):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    if habit_id is None:
        click.echo('Sorry, i am not so smart to predict which habit you want to see')
        return
    habit_id = str(habit_id)
    url = HOST + api + '/habits/' + habit_id
    habit_response = requests.get(url=url).json()
    if 'error' in habit_response:
        click.echo(habit_response['error'])
        return
    habit_info = (habit_id + ': ' + habit_response[habit_id]['name'] + '\nstatus: '
                  + habit_response[habit_id]['status'])
    if habit_response[habit_id]['timeline'] is not None:
        habit_info += '\ntimeline: ' + habit_response[habit_id]['timeline']
    click.echo(habit_info)
    return
