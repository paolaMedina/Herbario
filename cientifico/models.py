from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Cientifico(models.Model):
    nombre_completo = models.CharField(max_length=60)
    nombre_abreviado = models.CharField(blank=True,  null=True,default=None, max_length=30)
    unique_together  =  ( "nombre_completo" ,  "nombre_abreviado" )
