from django.db import models


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
    habits = models.Field.one_to_many(Habit)


class Event(models.Model):
    name = models.CharField(max_length=200, blank=False)
    event_date = models.DateTimeField()
    remember = models.Field.one_to_many(Remember)
    repeat = models.OneToOneField(Remember)
    comments = models.Field.one_to_many(Comment)


class Calender(models.Model):
    events = models.Field.one_to_many(Event)


class Subtask(models.Model):
    STATUS = (
        ('NS','NOT STARTED'),
        ('F', 'FINISHED')
    )
    name = models.CharField(max_length=200, blank=False)
    status = models.CharField(max_length=200, choices=STATUS)


class Task(models.Model):
    STATUS = (
        ('NS','NOT STARTED'),
        ('IP', 'IN PROCESS'),
        ('F', 'FINISHED')
    )
    name = models.CharField(max_length=200, blank=False)
    status = models.CharField(max_length=200, choices=STATUS)
    comments = models.Field.one_to_many(Comment)
    subtasks = models.Field.one_to_many(Subtask)
    deadline = models.DateTimeField()


class PrivateTask(models.Model):
    task = models.OneToOneField(Task)
    repeat = models.Field.one_to_many(WeeklyRepeat)
    remember = models.Field.one_to_many(Remember)


class WeeklyList(models.Model):
    name = models.CharField(max_length=200, blank=False)
    tasks = models.Field.one_to_many(PrivateTask)


class User(models.Model):
    email = models.EmailField(unique='True', blank=False)
    username = models.CharField(max_length=30, unique='True', blank=False)
    password_hash = models.CharField(max_length=200, blank=False)
    week_list = models.OneToOneField(WeeklyList)
    habit_tracker = models.OneToOneField(HabitTracker)
    calendar = models.OneToOneField(Calender)


class PublicTask(models.Model):
    task = models.OneToOneField(Task)
    executors = models.Field.one_to_many(User)


class List(models.Model):
    name = models.CharField(max_length=200, blank=False)
    tasks = models.Field.one_to_many(PrivateTask)
    accessors = models.Field.one_to_many(User)