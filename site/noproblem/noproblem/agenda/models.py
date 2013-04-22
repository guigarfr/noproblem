from django.db import models

class TipoEvento(models.Model):
	nombre = models.CharField(max_length=100)
	def __unicode__(self): 
		return self.nombre

class Evento(models.Model):
	tipo = models.ForeignKey(TipoEvento)
	titulo = models.CharField(max_length=100)
	contenido_generico = models.TextField()
	contenido_especifico = models.TextField(blank=True)
	fecha_ini = models.DateTimeField()
	fecha_final= models.DateTimeField()
	dia_entero = models.BooleanField()
	lugar = models.CharField(max_length=100)
	direccion=models.CharField(max_length=100)
	enlace_direccion = models.URLField(max_length=200,blank=True)
	ciudad=models.CharField(max_length=100)
	def __unicode__(self): 
		return self.titulo
	
