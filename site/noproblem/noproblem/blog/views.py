from django.shortcuts import render_to_response, render
from django.template import RequestContext
from noproblem.agenda.models import Evento
from django.template import Context
import datetime

def bloggy(request):
	hoy=datetime.datetime.now().date()
	ultimos_eventos = Evento.objects.filter(fecha_ini__lte=hoy).order_by('fecha_ini')[:5]
	context = Context({
					  'ultimos_eventos':ultimos_eventos,
					  })
	return render(request,'bloggy.html',context)
    #return render_to_response('bloggy.html', context_instance=RequestContext(request))
