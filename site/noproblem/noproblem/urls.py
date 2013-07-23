from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.static import *
#from noproblem.views import current_datetime, hours_ahead
from noproblem import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.preinicio),
	url('^welcome/$', views.preinicio),
	url('^inicio/$', views.inicio),
	url('^about/$', views.about),
	# divulgacion/blog debe ir antes porque es mas especifico que divulgacion a secas
	url(r'^divulgacion/blog/', include('noproblem.blog.urls', namespace="divulgacion/blog")),
	url('^divulgacion/$', views.divulgacion),
	url('^didactica/$', views.didactica),
	url('^desarrollo/$', views.desarrollo),
	url('^contacto/$', views.contacto, name="contacto"),

	# Aplicación Accounts
	url(r'^accounts/', include('noproblem.accounts.urls', namespace="accounts")), 

	# Aplicación Problemas
	url(r'^problems/', include('noproblem.problems.urls', namespace="problems")), 
                      
	# Admin and Admin Documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
    
    # Media files
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
     
)