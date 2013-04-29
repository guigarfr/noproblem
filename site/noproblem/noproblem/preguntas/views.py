from django.shortcuts import render
from noproblem.preguntas.models import Pregunta
from django.template import Context
import datetime

def ultimas_preguntas(request):
	hoy=datetime.datetime.now().date()
	ultimas = Pregunta.objects.filter(fecha__lte=hoy).order_by('-fecha')[:5]
	context = Context({
					  'ultimas':ultimas, 
					  })
	return render(request,'prueba.html',context)

