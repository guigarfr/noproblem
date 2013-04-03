from django.shortcuts import render_to_response
from django.template import RequestContext

def bloggy(request):
    return render_to_response('bloggy.html', context_instance=RequestContext(request))
