# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponse
# import datetime
# 
# def current_datetime(request):
#     now = datetime.datetime.now()
#     t = get_template('current_datetime.html')
#     html = t.render(Context({'current_date': now}))
#     return HttpResponse(html)
from django.shortcuts import render_to_response
import datetime
from django.template import RequestContext

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now}, context_instance=RequestContext(request))
    
def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	return render_to_response('hours_ahead.html', {'hour_offset': offset,'next_time': dt}, context_instance=RequestContext(request))
