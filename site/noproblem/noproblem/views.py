from django.shortcuts import render_to_response
from django.template import RequestContext

def inicio(request):
    return render_to_response('inicio.html', context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
    
def divulgacion(request):
    return render_to_response('divulgacion.html', context_instance=RequestContext(request))
    
def didactica(request):
    return render_to_response('didactica.html', context_instance=RequestContext(request))
    
def desarrollo(request):
    return render_to_response('desarrollo.html', context_instance=RequestContext(request))
    
def contacto(request):
    return render_to_response('contacto.html', context_instance=RequestContext(request))

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
