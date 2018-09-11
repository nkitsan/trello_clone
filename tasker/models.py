from django.db import models
from django.utils.crypto import get_random_string


class Comment(models.Model):
    comment = models.TextField()


class Remember(models.Model):
    repeat_date = models.DateTimeField()


class WeeklyRepeat(models.Model):
    repeat = models.SmallIntegerField()


class Habit(models.Model):
    STATUS = (
        ('NS','NOT STARTED'),
        ('F', 'FINISHED')
    )
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS, default='NS')
    timeline = models.IntegerField(default=21)
    count = models.IntegerField(default=0)


class Event(models.Model):
    name = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    remember = models.ManyToManyField(Remember)
    comments = models.ManyToManyField(Comment)


class Subtask(models.Model):
    STATUS = (
        ('NS','NOT STARTED'),
        ('F', 'FINISHED')
    )
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS, default='NS')


class Task(models.Model):
    STATUS = (
        ('NS','NOT STARTED'),
        ('IP', 'IN PROCESS'),
        ('F', 'FINISHED')
    )
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS, default='NS')
    comments = models.ManyToManyField(Comment)
    subtasks = models.ManyToManyField(Subtask)
    deadline = models.DateTimeField(blank=True, null=True)


class PrivateTask(models.Model):
    task = models.OneToOneField(Task)
    repeat = models.ManyToManyField(WeeklyRepeat)
    remember = models.ManyToManyField(Remember)
    display = models.BooleanField(default=True)


class User(models.Model):
    email = models.EmailField(unique=True)
    api_key = models.CharField(max_length=32, blank=True)
    username = models.CharField(max_length=30, unique=True)
    password_hash = models.CharField(max_length=200)
    week_list = models.ManyToManyField(PrivateTask)
    lists = models.ManyToManyField('List')
    habit_tracker = models.ManyToManyField(Habit)
    calendar = models.ManyToManyField(Event)
    update = models.DateTimeField(default=None, null=True)

    def generate_api_key(self):
        self.api_key = get_random_string(length=32)

    def __str__(self):
        return self.username


class PublicTask(models.Model):
    task = models.OneToOneField(Task)
    executors = models.ManyToManyField(User)


class List(models.Model):
    name = models.CharField(max_length=200)
    tasks = models.ManyToManyField(PublicTask)