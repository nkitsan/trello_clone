from tasker.libs.managers import user_manager
from django.utils import timezone
import datetime


def check_updates(username):
    user = user_manager.get_user(username)
    date = datetime.datetime.now(tz=timezone.utc)
    day = date.day
    month = date.month
    year = date.year
    if user.update is None or user.update.day != day:
        restart_habit(user)
        on_display(user)
        user.update = date
        user.save()
    elif user.update.day == day and user.update.month != month:
        restart_habit(user)
        on_display(user)
        user.update = date
        user.save()
    elif user.update.day == day and user.update.month == month and user.update.year != year:
        restart_habit(user)
        on_display(user)
        user.update = date
        user.save()


def restart_habit(user):
        for habit in user.habit_tracker.all():
            if habit.count < habit.timeline:
                habit.status = 'NS'
                habit.save()


def on_display(user):
        for task in user.week_list.all():
            repeat_exists = False
            count = 0
            for repeat in task.repeat.all():
                count += 1
                if repeat.repeat == datetime.datetime.now(tz=timezone.utc).weekday():
                    repeat_exists = True
            if not repeat_exists and count != 0:
                task.display = False
                task.save()
            if repeat_exists:
                task.display = True
                task.save()