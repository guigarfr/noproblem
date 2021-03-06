from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect 
from noproblem.forms import ContactForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from noproblem.agenda.models import Evento
from django.template import Context
import datetime

def preinicio(request):
    return render_to_response('preinicio.html', context_instance=RequestContext(request))

def inicio(request):
	hoy=datetime.datetime.now().date()
	ultimos_eventos = Evento.objects.filter(fecha_ini__gte=hoy).order_by('fecha_ini')[:5]
	pasados_eventos = Evento.objects.filter(fecha_ini__lte=hoy).order_by('fecha_ini')[:5]
	context = Context({
					  'ultimos_eventos':ultimos_eventos,'pasados_eventos':pasados_eventos,
					  })
	return render(request,'inicio.html',context)

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
    
def divulgacion(request):
    return render_to_response('divulgacion.html', context_instance=RequestContext(request))
    
def didactica(request):
    return render_to_response('didactica.html', context_instance=RequestContext(request))
    
def desarrollo(request):
    return render_to_response('desarrollo.html', context_instance=RequestContext(request))

def contacto(request):
	if request.method == 'POST': 
		form = ContactForm(request.POST) 
		if form.is_valid():
			messages.success(request, 'El formulario ha sido enviado')
			cd = form.cleaned_data 
			email = EmailMessage('[connectacpc] Contacto: ' + cd['nombre'] + ' motivo: ' + cd['motivo'],
								 cd['message'] + "\n\nEnviado por: " + cd.get('email'),
								 cd.get('email'),
								 ['guigarfr@gmail.com','paulatuzon@gmail.com'],
								 headers={'Reply-To': cd.get('email')})
			email.send()
			return render_to_response('contacto.html', {'form': form}, context_instance=RequestContext(request)) 
	else: 
		form = ContactForm() 
	return render_to_response('contacto.html', {'form': form}, context_instance=RequestContext(request)) 

#import datetime
# def current_datetime(request):
#     now = datetime.datetime.now()
#     return render_to_response('current_datetime.html', {'current_date': now}, context_instance=RequestContext(request))
#     
# def hours_ahead(request, offset):
# 	try:
# 		offset = int(offset)
# 	except ValueError:
# 		raise Http404()
# 	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
# 	return render_to_response('hours_ahead.html', {'hour_offset': offset,'next_time': dt}, context_instance=RequestContext(request))
