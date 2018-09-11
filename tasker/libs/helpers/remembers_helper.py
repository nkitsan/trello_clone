from tasker.libs.managers import weekly_task_manager
import datetime


def check_remembers(username):
    tasks = weekly_task_manager.get_weekly_tasks(username)
    remembers = []
    for task in tasks:
        for remember in task.remember.all():
            if remember.repeat_date <= datetime.datetime.now(datetime.timezone.utc) and task.display:
                remembers.append({'name': task.task.name, 'id': task.id, 'date': remember.repeat_date})
    return remembers
