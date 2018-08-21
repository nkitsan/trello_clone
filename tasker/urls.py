from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.user_board, name='user_board'),
]