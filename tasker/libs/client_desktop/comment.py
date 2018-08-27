import requests
from .config import host


def add_comment(api, event_id, list_id, task_id, text_comment):
    data = {'comment': text_comment}
    if event_id is not None:
        url = host + api + '/events/' + str(task_id)
        response_comment = requests.post(url=url, data=data).json()
        if response_comment['error'] is None:
            comment_id = response_comment[event_id]['comments'].keys()[0]
            return comment_id + ' ' + text_comment
    elif list_id is not None:
        url = host + api + '/lists/' + str(list_id) + '/tasks/' + str(task_id)
        response_comment = requests.post(url=url, data=data).json()
    else:
        url = host + api + '/tasks/' + str(task_id)
        response_comment = requests.post(url=url, data=data).json()
    if response_comment['error'] is not None:
        return response_comment['error']
    comment_id = response_comment[task_id]['comments'].keys()[0]
    return comment_id + ' ' + text_comment


def delete_comment(api, event_id, list_id, task_id, comment_id):
    data = {'comment_id': comment_id}
    if event_id is not None:
        url = host + api + '/events/' + str(task_id)
        response_comment = requests.delete(url=url, data=data).json()
    elif list_id is not None:
        url = host + api + '/lists/' + str(list_id) + '/tasks/' + str(task_id)
        response_comment = requests.delete(url=url, data=data).json()
    else:
        url = host + api + '/tasks/' + str(task_id)
        response_comment = requests.delete(url=url, data=data).json()
    if response_comment['error'] is not None:
        return response_comment['error']
    return 'comment was deleted successfully'


def show_comments(api, event_id, list_id, task_id):
    comments = {}
    if event_id is not None:
        url = host + api + '/events/' + str(task_id)
        response_comment = requests.get(url=url).json()
        if response_comment['error'] is None:
            comments = response_comment[event_id]['comments']
    elif list_id is not None:
        url = host + api + '/lists/' + str(list_id) + '/tasks/' + str(task_id)
        response_comment = requests.get(url=url).json()
    else:
        url = host + api + '/tasks/' + str(task_id)
        response_comment = requests.get(url=url).json()
    if response_comment['error'] is not None:
        return response_comment['error']
    if len(comments) == 0:
        comments = response_comment[task_id]['comments']
    result = ''
    for comment_id in comments:
        result += comment_id + ': ' + comments[comment_id] + '\n'
    return result


