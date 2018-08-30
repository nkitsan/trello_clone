import requests
import click
from .helper import HOST, api


@click.group()
def repeat_operations():
    """Here is commands which you can use to manipulate with repeat of tasks in private (weekly task) list"""


@repeat_operations.command(short_help='Create a new repeat for the task')
@click.option('--task_id', default=None, type=click.INT,
              help='ID of the task to add a repeat')
@click.option('--repeat', default=None, type=click.IntRange(0, 6), help='Repeat of task in week')
def add_repeat(task_id, repeat):
    if task_id is None:
        click.echo('You missed ID of task, to which you want to add a repeat')
        return
    if repeat is None:
        click.echo('You forgot repeat. We are not Vanga please add it')
    data = {'repeat': str(repeat)}
    url = HOST + api + '/tasks/' + str(task_id)
    response_repeat = requests.post(url=url, data=data).json()
    if 'error' in response_repeat:
        click.echo(response_repeat['error'])
        return
    click.echo('repeat was successfully added')
    return


@repeat_operations.command(short_help='Delete the repeat from the task')
@click.option('--task_id', default=None, type=click.INT, help='ID of the task to delete a repeat')
@click.option('--repeat_id', default=None, type=click.INT, help='ID of the repeat to delete')
def delete_repeat(task_id, repeat_id):
    if task_id is None:
        click.echo('You missed ID of task, in which you want to delete the repeat')
        return
    if repeat_id is None:
        click.echo('You forgot a repeat ID. We are not Vanga please add it')
    data = {'repeat_id': str(repeat_id)}
    url = HOST + api + '/tasks/' + str(task_id)
    response_repeat = requests.delete(url=url, data=data).json()
    if 'error' in response_repeat:
        click.echo(response_repeat['error'])
        return
    click.echo('repeat was successfully deleted')
    return


@repeat_operations.command(short_help='Show repeats of the task')
@click.option('--task_id', default=None, type=click.INT, help='ID of the task to show repeats')
def show_repeats(task_id):
    if task_id is None:
        click.echo('You missed ID of task, in which you want to delete the repeat')
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
