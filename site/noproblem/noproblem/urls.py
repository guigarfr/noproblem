from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.static import *
#from noproblem.views import current_datetime, hours_ahead
from noproblem.views import inicio, about, divulgacion, didactica, desarrollo, contacto

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	('^inicio/$', inicio),
    ('^about/$', about),
    ('^divulgacion/$', divulgacion),
    ('^didactica/$', didactica),
    ('^desarrollo/$', desarrollo),
    ('^contacto/$', contacto),
    # Examples:
    #('^time/$', current_datetime),
    #(r'^time/plus/(\d{1,2})/$', hours_ahead),
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),
    url(r'^problems/', include('noproblem.problems.urls', namespace="problems")),
                       
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
     
)