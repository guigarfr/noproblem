from django import template
from django.shortcuts import render
from django.template import Context, Library, Node
from noproblem.preguntas.models import Pregunta
import datetime
from django.db import models

register = template.Library()
	
def ultimas_preguntas():
	hoy=datetime.datetime.now().date()
	ultimas = Pregunta.objects.filter(fecha__lte=hoy).order_by('-fecha')[:5]
	return {'ultimas':ultimas}
					  
register.inclusion_tag('prueba.html')(ultimas_preguntas)