import requests
import click
from .helper import HOST
from .access import read_api


@click.group()
def subtask_operations():
    """Here is commands which you can use to manipulate with subtasks of tasks in public and private lists"""


@subtask_operations.command(short_help='Create a new subtask of the task')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list in which the task for subtask is placed. Skip: add to the weekly tasks list')
@click.option('--task_id', required=True, type=click.INT, help='ID of the task in which you want to create a subtask')
@click.option('--subtask', default='', help='Name of a created subtask')
def add_subtask(list_id, task_id, subtask):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    data = {'subtask': subtask}
    task_id = str(task_id)
    if list_id is None:
        url = HOST + api + '/tasks/' + task_id
        response_subtask = requests.post(url=url, data=data).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + task_id
        response_subtask = requests.post(url=url, data=data).json()
    if 'error' in response_subtask:
        click.echo(response_subtask['error'])
        return
    click.echo('subtask was successfully added')
    return


@subtask_operations.command(short_help='delete the subtask from the task')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list, in which you are going to delete the task. Skip: delete in the weekly tasks list')
@click.option('--task_id', required=True, type=click.INT, help='ID of the task, in which you want to delete the subtask')
@click.option('--subtask_id', required=True, type=click.INT, help='ID of the subtask, which you want to delete')
def delete_subtask(list_id, task_id, subtask_id):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    subtask_id = str(subtask_id)
    task_id = str(task_id)
    data = {'subtask_id': subtask_id}
    if list_id is None:
        url = HOST + api + '/tasks/' + task_id
        response_subtask = requests.delete(url=url, data=data).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + task_id
        response_subtask = requests.delete(url=url, data=data).json()
    if 'error' in response_subtask:
        click.echo(response_subtask['error'])
        return
    click.echo('subtask was successfully deleted')
    return


@subtask_operations.command(short_help='Change status of the subtask')
@click.option('--list_id', default=None, type=click.INT,
              help="""ID of the list in which you want to change the task subtask status. 
              Skip: change in the weekly tasks list""")
@click.option('--task_id', required=True, type=click.INT, help='ID of task in which you want to change subtask status')
@click.option('--subtask_id', required=True, type=click.INT, help='ID of subtask in which you want to change status')
@click.option('--status', required=True, type=click.Choice(['NS', 'F']), help='New status of the subtask')
def change_subtask(list_id, task_id, subtask_id, status):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    task_id = str(task_id)
    subtask_id = str(subtask_id)
    data = {'subtask_id': subtask_id, 'subtask_status': status}
    if list_id is None:
        url = HOST + api + '/tasks/' + task_id
        response_subtask = requests.put(url=url, data=data).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + task_id
        response_subtask = requests.put(url=url, data=data).json()
    if 'error' in response_subtask:
        click.echo(response_subtask['error'])
        return
    click.echo('subtask status was successfully changed')
    return


@subtask_operations.command(short_help='Show subtasks of the task')
@click.option('--list_id', default=None, type=click.INT,
              help="""ID of the list, in which you want to see subtasks of the task. 
              Skip: see subtasks of the task in the weekly tasks list""")
@click.option('--task_id', required=True, type=click.INT,
              help='ID of the list, in which you want to see tasks. Skip: see tasks in the weekly tasks list')
def show_subtasks(list_id, task_id):
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    task_id = str(task_id)
    if list_id is None:
        url = HOST + api + '/tasks/' + task_id
        response_subtask = requests.get(url=url).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + task_id
        response_subtask = requests.get(url=url).json()
    if 'error' in response_subtask:
        click.echo(response_subtask['error'])
        return
    subtasks = response_subtask[task_id]['subtasks']
    result = ''
    for subtask_id in subtasks:
        result += (subtask_id + ': ' + subtasks[subtask_id]['name'] + '\nstatus: ' + subtasks[subtask_id]['status']
                   + '\n\n')
    if result == '':
        click.echo('No subtasks in task')
        return
    click.echo(result.rstrip('\n'))
    return
