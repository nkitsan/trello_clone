import requests
import click
import string
from .helper import HOST


@click.group()
def access_operations():
    """Here is commands which can allow to add access to lists and define executors of tasks"""


@access_operations.command(short_help='add user to list or executor to task')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list, in which you are going to add the executor.')
@click.option('--task_id', default=None, type=click.INT,
              help='ID of the task in which you want to add executor. Skip: add access to list')
@click.option('--username', default=None, help='Username of user which you want to add')
def add_user(list_id, task_id, username):
    if list_id is None and list_id is None:
        click.echo('You missed the ID of a task or a list to which you want to add user')
        return
    if username is None:
        click.echo('No username to add user')
        return
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    if task_id is None:
        url = HOST + api + '/lists/' + str(list_id)
        data = {'new_user': username}
        response = requests.post(url=url, data=data).json()
        if 'error' not in response:
            click.echo('list was added successfully to user lists')
            return
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + str(task_id)
        data = {'executor': username}
        response = requests.post(url=url, data=data).json()
    if 'error' in response:
        click.echo(response['error'])
        return
    click.echo('executor was successfully added')
    return


@access_operations.command(short_help='delete user access from list or executor from task')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list, in which you are going to delete the executor.')
@click.option('--task_id', default=None, type=click.INT,
              help='ID of the task in which you want to delete executor. Skip: delete access to list')
@click.option('--username', default=None, help='Username of user whose access should be limited')
def delete_user(list_id, task_id, username):
    if list_id is None and list_id is None:
        click.echo('You missed the ID of a task or a list in which you want to delete user')
        return
    if username is None:
        click.echo('No username to delete user')
        return
    api = read_api()
    if api is None:
        click.echo('Use login --api to register your api key and work further')
        return
    if task_id is None:
        url = HOST + api + '/lists/' + str(list_id)
        data = {'new_user': username}
        response = requests.delete(url=url, data=data).json()
        if 'error' not in response:
            click.echo('list was deleted successfully from user lists')
            return
    else:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + str(task_id)
        data = {'executor': username}
        response = requests.delete(url=url, data=data).json()
    if 'error' in response:
        click.echo(response['error'])
        return
    click.echo('executor was successfully deleted')
    return


@access_operations.command(short_help='Add api key from account to begin')
@click.option('--api', default=None, help='Api key from account')
def login(api):
    allowed = string.digits + string.ascii_letters
    if all(c in allowed for c in api):
        with open("api.txt", "w+") as api_file:
            api_file.write(api)
        click.echo('api key was successfully added')
    else:
        click.echo('wrong api key')
    return


def read_api():
    try:
        api_file = open("api.txt", "r+")
    except IOError:
        return None
    else:
        api = api_file.readline()
        api_file.close()
    return api
