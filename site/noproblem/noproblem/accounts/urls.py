from django.conf.urls import patterns, url
from noproblem.accounts import views

urlpatterns = patterns('',
                       # ex: /accounts/
                       #url(r'^$', views.index, name='index'),
                       # ex: /accounts/login/
                       url(r'^login/$', views.login_user),
                       url(r'^logout/$', views.logout, name='auth_logout_user'),
                       url(r'^register$', views.register_user, name='register'),
)