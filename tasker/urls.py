from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.user_board, name='user_board'),
    url(r'^(?P<api>[\w\-]+)/habits/(?P<habit_id>\d+)/$', views.habit_api, name='habit_api'),
    url(r'^(?P<api>[\w\-]+)/events/(?P<event_id>\d+)/$', views.event_api, name='event_api'),
    url(r'^(?P<api>[\w\-]+)/tasks/(?P<task_id>\d+)/$', views.private_task_api, name='private_task_api'),
    url(r'^(?P<api>[\w\-]+)/lists/(?P<list_id>\d+)/tasks/(?P<task_id>\d+)/$', views.public_task_api,
        name='public_task_api'),
    url(r'^(?P<api>[\w\-]+)/lists/(?P<list_id>\d+)/$', views.list_api, name='list_api'),
    url(r'^(?P<api>[\w\-]+)/habits/$', views.habits_api, name='habits_api'),
    url(r'^(?P<api>[\w\-]+)/events/$', views.events_api, name='events_api'),
    url(r'^(?P<api>[\w\-]+)/tasks/$', views.private_tasks_api, name='private_tasks_api'),
    url(r'^(?P<api>[\w\-]+)/lists/(?P<list_id>\d+)/tasks/$', views.public_tasks_api, name='public_tasks_api'),
    url(r'^(?P<api>[\w\-]+)/lists/$', views.list_api, name='lists_api'),
]