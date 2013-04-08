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
)

#urlpatterns = patterns('',
#                       url(r'^$',
#                           ListView.as_view(
#                                            queryset=Problem.objects.order_by('-pub_date')[:5],
#                                            context_object_name='latest_prob_list',
#                                            template_name='index.html'),
#                           name='index'),
#                       url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Problem, template_name='detail.html'), name='detail'),
#                       url(r'^(?P<pk>\d+)/results/$',
#                           DetailView.as_view(
#                                              model=Problem,
#                                              template_name='stats.html'),
#                           name='stats'),
#                       )
