from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from noproblem.problems.models import Problem
from noproblem.problems import views

urlpatterns = patterns('',
                       # ex: /problems/
                       url(r'^$', views.index, name='main'),
)

