from django.db import models

class Pregunta(models.Model):
	cuestion = models.TextField()
	respuesta = models.TextField(blank=True)
	fecha = models.DateTimeField()
	enlace = models.URLField(max_length=200,blank=True)
	usuario = models.CharField(max_length=100,blank=True)
	def __unicode__(self): 
		return self.fecha.strftime("%d-%m-%Y")
	
