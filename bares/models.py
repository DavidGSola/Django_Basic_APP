import datetime
from django.utils import timezone
from django.db import models

# Create your models here.

class Bares(models.Model):
	nombre = models.CharField(max_length=200)
	direccion = models.CharField(max_length=200)
	fecha_visita = models.DateTimeField('Fecha visita')
	
	def __unicode__(self):
		return self.nombre
		
	def fue_visitada_recientemente(self):
		return self.fecha_visita >= timezone.now() - datetime.timedelta(days=1)
		
class Tapas(models.Model):
	bar = models.ForeignKey(Bares)
	tapa = models.CharField(max_length=200)
	votos = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.tapa
