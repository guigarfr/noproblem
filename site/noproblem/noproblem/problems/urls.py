from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from noproblem.problems.models import Problem
from noproblem.problems import views

urlpatterns = patterns('',
                       # ex: /problems/
                       url(r'^$', views.index, name='index'),
                       # ex: /problems/5/
                       url(r'^(?P<prob_id>\d+)/$', views.detail, name='detail'),
                       # ex: /problems/5/stats/
                       url(r'^(?P<prob_id>\d+)/stats/$', views.stats, name='stats'),
                       # ex: /problems/5/solve/
                       url(r'^(?P<prob_id>\d+)/solve/$', views.solve, name='solve'),
                       # ex: /problems/5/send/
                       url(r'^(?P<prob_id>\d+)/send/$', views.sendresult, name='sendresult'),
                       # ex: /problems/user_detail/
                       url(r'^user_detail/$', views.user_detail, name='user_detail'),
                       # ex: /problems/tree/
                       url(r'^tree/(?P<cat_id>\d+)/$', views.tree, name='tree'),
                       url(r'^bienvenida/$', views.bienvenida, name='bienvenida'),
                       url(r'^bienvenida/contacto/$', views.contacto, name='contacto'),
)
