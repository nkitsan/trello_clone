from django.test import TestCase
from tasker.libs.managers import calendar_manager
from django.contrib.auth.hashers import make_password
from tasker.models import User, Event
import datetime


class TaskManagerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='example', email='examle@post.com',
                                        password_hash=make_password('1111'))
        self.event = self.user.calendar.create(name='test event', event_date=(datetime.datetime.now()                                                                     + datetime.timedelta(days=7)))

    def test_add_event_remember(self):
        remember = calendar_manager.add_event_remember(self.user.username, self.event.id,
                                            self.event.event_date - datetime.timedelta(days=1))
        self.assertIsNotNone(remember)