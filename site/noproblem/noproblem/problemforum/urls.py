from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from noproblem.problems.models import Problem
from noproblem.problemforum import views

urlpatterns = patterns('',
	url(r'^$', views.forum, name='index'),
	url(r'^thread/(\d+)/$', views.thread, name='thread'),
	url(r'^post/(new_message|reply)/(\d+)/$', views.post, name='post'),
	url(r'^reply/(\d+)/$', views.reply, name='reply'),
	url(r'^new_message/(\d+)/$', views.new_message, name='new_message'),
	url(r'^pay/(\d+)/$', views.payforumentrance, name='payforumentrance'),
)
