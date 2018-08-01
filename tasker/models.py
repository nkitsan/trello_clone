from django.db import models


class Comment(models.Model):
    comment = models.TextField()


class Date(models.Model):
    repeat_date = models.DateTimeField()


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


class Habbit(models.Model):
    STATUS = (
        ('NS','NOT STARTED'),
        ('F', 'FINISHED')
    )
    name = models.CharField(max_length=200, blank=False)
    status = models.CharField(max_length=200, choices=STATUS)
    timeline = models.IntegerField()


class Event(models.Model):
    name = models.CharField(max_length=200, blank=False)
    event_date = models.DateTimeField()
    repeat = models.Field.one_to_many(Date)
    comments = models.Field.one_to_many(Comment)


class User(models.Model):
    email = models.EmailField(unique='True', blank=False)
    username = models.CharField(max_length=30, unique='True', blank=False)
    password_hash = models.CharField(max_length=200, blank=False)