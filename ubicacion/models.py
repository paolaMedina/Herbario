
from __future__ import unicode_literals

from django.db import models

# Create your models here.

type_pos_Lat = (('ninguno', 'Ninguno'),('N', 'Norte'), ('S', 'Sur'))
type_pos_Long = (('ninguno', 'Ninguno'),('E', 'Este'), ('W', 'Oeste'))


class Ubicacion(models.Model):
    pais = models.CharField(max_length=200,default=None,null=True)
    departamento= models.CharField(max_length=200,default=None,null=True)
    municipio= models.CharField(max_length=200,default=None,null=True)
    divisionPolitica= models.CharField(max_length=200,default=None,null=True)
    especificacionLocacion = models.TextField(default=None,null=True)
    latitud = models.FloatField(default=None,null=True)
    posicionLat = models.CharField(max_length=7, choices=type_pos_Lat, default='ninguno')
    longitud = models.FloatField(default=None,null=True)
    posicionLong = models.CharField(max_length=7, choices=type_pos_Long, default='ninguno')
    alturaMinima = models.FloatField(default=None,null=True)
    alturaMaxima = models.FloatField(default=None,null=True)
    altUni = models.CharField(max_length=20,null=True,default=None,)
    cultivada = models.BooleanField(default=True)