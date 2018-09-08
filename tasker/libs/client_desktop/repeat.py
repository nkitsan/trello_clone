import requests
import click
from .helper import HOST
from .access import read_api


@click.group()
def repeat_operations():
    """Here is commands which you can use to manipulate with repeat of tasks in private (weekly task) list"""


@repeat_operations.command(short_help='Create a new repeat for the task')
@click.option('--task_id', required=True, type=click.INT,
              help='ID of the task to add a repeat')
@click.option('--repeat', required=True, type=click.IntRange(0, 6), help='Repeat of task in week')
def add_repeat(task_id, repeat):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    data = {'repeat': str(repeat)}
    url = HOST + api + '/tasks/' + str(task_id)
    response_repeat = requests.post(url=url, data=data).json()
    if 'error' in response_repeat:
        click.echo(response_repeat['error'])
        return
    click.echo('repeat was successfully added')
    return


@repeat_operations.command(short_help='Delete the repeat from the task')
@click.option('--task_id', required=True, type=click.INT, help='ID of the task to delete a repeat')
@click.option('--repeat_id', required=True, type=click.INT, help='ID of the repeat to delete')
def delete_repeat(task_id, repeat_id):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    data = {'repeat_id': str(repeat_id)}
    url = HOST + api + '/tasks/' + str(task_id)
    response_repeat = requests.delete(url=url, data=data).json()
    if 'error' in response_repeat:
        click.echo(response_repeat['error'])
        return
    click.echo('repeat was successfully deleted')
    return


@repeat_operations.command(short_help='Show repeats of the task')
@click.option('--task_id', required=True, type=click.INT, help='ID of the task to show repeats')
def show_repeats(task_id):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    task_id = str(task_id)
    url = HOST + api + '/tasks/' + task_id
    response_repeat = requests.get(url=url).json()
    if 'error' in response_repeat:
        click.echo(response_repeat['error'])
        return
    result = ''
    repeats = response_repeat[task_id]['repeats']
    for repeat_id in repeats:
        result += repeat_id + ': ' + str(repeats[repeat_id]) + '\n'
    click.echo(result.rstrip('\n'))
    return
