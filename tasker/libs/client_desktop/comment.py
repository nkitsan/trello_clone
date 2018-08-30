import requests
import click
from .helper import HOST, api


@click.group()
def comment_operations():
    """Here is commands which you can use to manipulate with comments of tasks and events"""


@comment_operations.command(short_help='Create a new comment to a task')
@click.option('--event_id', default=None, type=click.INT, help='ID of the event to which you want to add the task')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list in which you want to add the comment. Skip: change in the weekly tasks list')
@click.option('--task_id', default=None, type=click.INT, help='ID of task to which you want to add the comment')
@click.option('--text', default='', help='Text of comment')
def add_comment(event_id, list_id, task_id, text):
    if event_id and task_id is None:
        click.echo('You forget to choose event or task id')
        return
    data = {'comment': text}
    task_id = str(task_id)
    if event_id is not None:
        url = HOST + api + '/events/' + str(event_id)
        response_comment = requests.post(url=url, data=data).json()
        if 'error' not in response_comment:
            comment_id = ''
            for key in response_comment:
                comment_id = key
            click.echo(comment_id + ' ' + text)
            return
    elif list_id is not None:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + task_id
        response_comment = requests.post(url=url, data=data).json()
    else:
        url = HOST + api + '/tasks/' + task_id
        response_comment = requests.post(url=url, data=data).json()
    if 'error' in response_comment:
        click.echo(response_comment['error'])
        return
    click.echo('comment was successfully added')
    return


@comment_operations.command(short_help='Delete a comment from a task')
@click.option('--event_id', default=None, type=click.INT,
              help='ID of the event in which you want to delete the comment')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list in which you want to delete the comment. Skip: change in the weekly tasks list')
@click.option('--task_id', default=None, type=click.INT, help='ID of the task in which you want to delete the comment')
@click.option('--comment_id', default=None, type=click.INT, help='ID of the comment which you want to delete')
def delete_comment(event_id, list_id, task_id, comment_id):
    if event_id and task_id is None:
        click.echo('You forget to choose event or task id')
        return
    task_id = str(task_id)
    data = {'comment_id': str(comment_id)}
    if event_id is not None:
        url = HOST + api + '/events/' + str(event_id)
        response_comment = requests.delete(url=url, data=data).json()
    elif list_id is not None:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + task_id
        response_comment = requests.delete(url=url, data=data).json()
    else:
        url = HOST + api + '/tasks/' + task_id
        response_comment = requests.delete(url=url, data=data).json()
    if 'error' in response_comment:
        click.echo(response_comment['error'])
        return
    click.echo('comment was deleted successfully')
    return


@comment_operations.command(short_help='Show a comment from a task')
@click.option('--event_id', default=None, type=click.INT,
              help='ID of the event in which you want to see the comment')
@click.option('--list_id', default=None, type=click.INT,
              help='ID of the list in which you want to see the comment. Skip: change in the weekly tasks list')
@click.option('--task_id', default=None, type=click.INT, help='ID of the task in which you want to see the comment')
def show_comments(event_id, list_id, task_id):
    if event_id and task_id is None:
        click.echo('You forget to choose event or task id')
        return
    comments = {}
    task_id = str(task_id)
    if event_id is not None:
        event_id = str(event_id)
        url = HOST + api + '/events/' + event_id
        response_comment = requests.get(url=url).json()
        if 'error' not in response_comment:
            comments = response_comment[event_id]['comments']
    elif list_id is not None:
        url = HOST + api + '/lists/' + str(list_id) + '/tasks/' + task_id
        response_comment = requests.get(url=url).json()
    else:
        url = HOST + api + '/tasks/' + task_id
        response_comment = requests.get(url=url).json()
    if 'error' in response_comment:
        click.echo(response_comment['error'])
        return
    if len(comments) == 0:
        comments = response_comment[task_id]['comments']
    result = ''
    for comment_id in comments:
        result += comment_id + ': ' + comments[comment_id] + '\n'
    click.echo(result)
    return
