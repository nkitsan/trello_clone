from tasker.libs.managers import weekly_task_manager, public_task_manager


weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


def task_repeats(username, task_id):
    """
    Transforms repeats from numbers to days of the week

    :param username: an username of an user
    :param task_id: an id of a task to take repeats
    :return: array of dicts with its an id and a day
    [{'id': repeat_id_1, 'day':'monday'},
    {'id': repeat_id_1, 'day':'tuesday'}...]
    """
    task = weekly_task_manager.find_user_task(username, task_id)
    repeats = []
    for repeat in task.repeat.all():
            repeats.append({'id': repeat.id, 'day': weekdays[repeat.repeat]})
    return repeats


def tasks_to_dict(username):
    """
    Transforms tasks from lists in a dictionary form

    :param username: an username of an user
    :return: lists and tasks in a format
    {list_name_1: {'id': list_id_1, 'tasks':[task_1, task_2...]},
    list_name_2: {'id': list_id_2, 'tasks':[task_1, task_2...]}}
    """
    lists = public_task_manager.get_user_lists(username)
    tasks_dict = {}
    for li in lists:
        tasks_dict.update({li.name: {'id': li.id, 'tasks': li.tasks.all()}})
    return tasks_dict

