from django.db import models
from django.utils.crypto import get_random_string


class Comment(models.Model):
    comment = models.TextField()


class Remember(models.Model):
    repeat_date = models.TimeField()


class WeeklyRepeat(models.Model):
    repeat = models.SmallIntegerField()


class Habit(models.Model):
    STATUS = (
        ('NS','NOT STARTED'),
        ('F', 'FINISHED')
    )
    name = models.CharField(max_length=200, blank=False)
    status = models.CharField(max_length=200, choices=STATUS)
    timeline = models.IntegerField()


class HabitTracker(models.Model):
    habits = models.ManyToManyField(Habit)


class Event(models.Model):
    name = models.CharField(max_length=200, blank=False)
    event_date = models.DateTimeField()
    remember = models.ManyToManyField(Remember)
    repeat = models.OneToOneField(Remember, related_name='period')
    comments = models.ManyToManyField(Comment)


class Calender(models.Model):
    events = models.ManyToManyField(Event)


class Subtask(models.Model):
    STATUS = (
        ('NS','NOT STARTED'),
        ('F', 'FINISHED')
    )
    name = models.CharField(max_length=200, blank=False)
    status = models.CharField(max_length=200, choices=STATUS, default='NS')


class Task(models.Model):
    STATUS = (
        ('NS','NOT STARTED'),
        ('IP', 'IN PROCESS'),
        ('F', 'FINISHED')
    )
    name = models.CharField(max_length=200, blank=False)
    status = models.CharField(max_length=200, choices=STATUS, default='NS')
    comments = models.ManyToManyField(Comment)
    subtasks = models.ManyToManyField(Subtask)
    deadline = models.DateTimeField(default=None)


class PrivateTask(models.Model):
    task = models.OneToOneField(Task)
    repeat = models.ManyToManyField(WeeklyRepeat)
    remember = models.ManyToManyField(Remember)


class WeeklyList(models.Model):
    name = models.CharField(max_length=200, blank=False)
    tasks = models.ManyToManyField(PrivateTask)


class User(models.Model):
    email = models.EmailField(unique=True, blank=False)
    api_key = models.CharField(max_length=32, unique=True)
    username = models.CharField(max_length=30, unique=True, blank=False)
    password_hash = models.CharField(max_length=200, blank=False)
    week_list = models.OneToOneField(WeeklyList)
    lists = models.ManyToManyField('List')
    habit_tracker = models.OneToOneField(HabitTracker)
    calendar = models.OneToOneField(Calender)

    def generate_api_key(self):
        self.api_key = get_random_string(length=32)

    def __str__(self):
        return self.username


class PublicTask(models.Model):
    task = models.OneToOneField(Task)
    executors = models.ManyToManyField(User)


class List(models.Model):
    name = models.CharField(max_length=200, blank=False)
    tasks = models.ManyToManyField(PrivateTask)