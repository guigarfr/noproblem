from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from noproblem.blog import views

urlpatterns = patterns('',
                       # ex: /divulgacion/blog/
                       url(r'^$', views.index, name='index'),
)

