from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from noproblem.preguntas.models import Pregunta
from noproblem.preguntas import views

urlpatterns = patterns('',
                       # ex: /problems/user_detail/
                       url(r'^ultimas/$', views.ultimas_preguntas, name='ultimas'),
)

