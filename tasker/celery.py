from .models import Habit, PrivateTask
import datetime


def restart_habit(self):
        for habit in Habit.objects.all():
            if habit.count < habit.timeline:
                habit.status = 'NS'
                habit.save()


def on_display(self):
        for task in PrivateTask.objects.all():
            repeat_exists = False
            for repeat in task.repeat.all():
                if repeat.repeat == datetime.datetime.now().weekday():
                    repeat_exists = True
            if not repeat_exists:
                task.display = False
            if repeat_exists:
                task.display = True
