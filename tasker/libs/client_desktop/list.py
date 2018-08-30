import requests
import click
from .helper import HOST, api


@click.group()
def list_operations():
    """Here is commands which you can use to manipulate with public list"""


@list_operations.command(short_help='Create a new list')
@click.option('--name', default='', help='Name of a created list')
def add_list(name):
    data = {'list_name': name}
    url = HOST + api + '/lists'
    list_response = requests.post(url=url, data=data).json()
    list_id = ''
    for key in list_response:
        list_id = key
    if 'error' in list_response:
        click.echo(list_response['error'])
        return
    click.echo(list_id + ': ' + list_response[list_id]['name'])
    return


@list_operations.command(short_help='Change a list name')
@click.option('--list_id', default=None, type=click.INT, help='ID of the list in which you want to change a name')
@click.option('--name', default='', help='Name to change a list name')
def change_list(list_id, name):
    if list_id is None:
        click.echo('Ups! You forget to choose list id')
        return
    list_id = str(list_id)
    data = {'list_name': name}
    url = HOST + api + '/lists/' + list_id
    list_response = requests.put(url=url, data=data).json()
    if 'error' in list_response:
        click.echo(list_response['error'])
        return
    click.echo(list_id + ': ' + list_response['4'])
    return


@list_operations.command(short_help='Delete a list')
@click.option('--list_id', default=None, type=click.INT, help='ID of the list which you want to delete')
def delete_list(list_id):
    if list_id is None:
        click.echo('Ups! You forget to choose list id')
        return
    data = {'list_id': str(list_id)}
    url = HOST + api + '/lists'
    list_response = requests.delete(url=url, data=data).json()
    if 'error' in list_response:
        click.echo(list_response['error'])
        return
    click.echo('list was deleted successfully')
    return


@list_operations.command(short_help='Show user public list')
def show_lists():
    url = HOST + api + '/lists'
    list_response = requests.get(url=url).json()
    if 'error' in list_response:
        click.echo(list_response['error'])
        return
    lists = ''
    for list_id in list_response:
        lists += list_id + ': ' + list_response[list_id]['name'] + '\n'
    if lists == '':
        click.echo('You do not have public lists. But good news, you can create it')
        return
    click.echo(lists.rstrip('\n'))
    return
