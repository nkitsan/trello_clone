import requests
import click
from .helper import HOST, date_validation, api


@click.group()
def task_operations():
    """Here is commands which you can use to manipulate with tasks in public and private lists"""


@task_operations.command(short_help='Create a new task in the list')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list in which you want to create a task. Skip: add to the weekly tasks list')
@click.option('--name', default='', help='Name of a created task')
def add_task(list_id, name):
    data = {'task_name': name}
    if list_id is None:
        url = HOST + api + '/tasks'
        task_response = requests.post(url=url, data=data).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks'
        task_response = requests.post(url=url, data=data).json()
    if 'error' in task_response:
        click.echo(task_response['error'])
        return
    task_id = ''
    for key in task_response:
        task_id = key
    click.echo(task_id + ' ' + task_response[task_id]['name'])
    return


@task_operations.command(short_help='Change the task in the list')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list in which you want to change the task. Skip: change in the weekly tasks list')
@click.option('--task_id', default=None, type=click.INT, help='ID of task in which you want to change')
@click.option('--name', default=None, help='New name of the task')
@click.option('--status', default=None, type=click.Choice(['NS', 'IP', 'F']), help='New status of the task')
@click.option('--deadline', default=None, help='New deadline of the task')
def change_task(list_id, task_id, name, status, deadline):
    if task_id is None:
        click.echo('You missed ID of task, which you want to change')
        return
    data = {}
    task_id = str(task_id)
    if name is not None:
        data.update({'task_name': name})
    if status is not None:
        data.update({'task_status': status})
    if deadline is not None and date_validation(deadline):
        data.update({'task_deadline': deadline})
    if list_id is None:
        url = HOST + api + '/tasks/' + task_id
        task_response = requests.put(url=url, data=data).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + task_id
        task_response = requests.put(url=url, data=data).json()
    if 'error' in task_response:
        click.echo(task_response['error'])
        return
    click.echo(task_id + ': ' + task_response[task_id]['name'] + '\nstatus: ' + task_response[task_id]['status'])
    if task_response[task_id]['deadline'] is not None:
        click.echo('deadline: ' + ' '.join(task_response[task_id]['deadline'][0:-1].split('T')))
    return


@task_operations.command(short_help='delete task from list')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list, in which you are going to delete the task. Skip: delete in the weekly tasks list')
@click.option('--task_id', default=None, type=click.INT, help='ID of the task, which you want to delete')
def delete_task(list_id, task_id):
    if task_id is None:
        click.echo('You missed the ID of the task, which you want to delete')
        return
    task_id = str(task_id)
    data = {'task_id': task_id}
    if list_id is None:
        url = HOST + api + '/tasks'
        task_response = requests.delete(url=url, data=data).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks'
        task_response = requests.delete(url=url, data=data).json()
    if 'error' in task_response:
        click.echo(task_response['error'])
        return
    click.echo('task was deleted successfully')
    return


@task_operations.command(short_help='Show tasks from the list')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list, in which you want to see tasks. Skip: see tasks in the weekly tasks list')
def show_tasks(list_id):
    if list_id is None:
        url = HOST + api + '/tasks'
        task_response = requests.get(url=url).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks'
        task_response = requests.get(url=url).json()
    if 'error' in task_response:
        click.echo(task_response['error'])
        return
    tasks = ''
    for task_id in task_response:
        tasks += task_id + ' ' + task_response[task_id]['name'] + '\n'
    click.echo(tasks.rstrip('\n'))
    return


@task_operations.command(short_help='Show the task from the list')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of list in which you want to see the task. Skip: see the task from the weekly tasks list')
@click.option('--task_id', default=None, type=click.INT, help='ID of the task, which you want to see')
def show_task(list_id, task_id):
    if task_id is None:
        click.echo('You missed the ID of the task, which you want to delete')
        return
    task_id = str(task_id)
    if list_id is None:
        url = HOST + api + '/tasks/' + task_id
        task_response = requests.get(url=url).json()
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + task_id
        task_response = requests.get(url=url).json()
    if 'error' in task_response:
        click.echo(task_response['error'])
        return
    task = task_id + ' ' + task_response[task_id]['name'] + '\nstatus: ' + task_response[task_id]['status'] + '\n'
    if task_response[task_id]['deadline'] is not None:
        task += 'deadline: ' + ' '.join(task_response[task_id]['deadline'][0:-1].split('T'))
    if list_id is not None:
        task += '\nexecutors:'
        for executor in task_response[task_id]['executors']:
            task += ' ' + executor
    click.echo(task.rstrip('\n'))
    return
