from django.conf.urls import url, include
from .import views


app_name = 'Qrious'

urlpatterns = [

    
	# /
    url(r'^$', views.main, name='main'),
    # /<number>/
    url(r'^(?P<number>[0-9]+)/$', views.detail, name='detail'),
    # /<number>/answer/
    url(r'^(?P<number>[0-9]+)/answer/$', views.answer, name='answer'),
    # /<number>/skip/
    url(r'^(?P<number>[0-9]+)/skip/$', views.skip, name='skip'),
    # /<number>/leave/
    url(r'^(?P<number>[0-9]+)/leave/$', views.leave, name='leave'),
    # /leaderboard/
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    # /main/
    url(r'^main/$', views.main, name='main'),




            ]
