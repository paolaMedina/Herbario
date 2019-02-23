from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Ubicacion(models.Model):
    pais = models.CharField(max_length=200,null=True)
    departamento= models.CharField(max_length=200,null=True)
    municipio= models.CharField(max_length=200,null=True)
    divisionPolitica= models.CharField(max_length=200,default=None,null=True)
    latitud = models.FloatField(default=None,null=True)
    longitud = models.FloatField(default=None,null=True)
    especificacionLocacion = models.TextField(default=None,null=True)
    cultivada = models.BooleanField(default=True)