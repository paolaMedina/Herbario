from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Ubicacion(models.Model):
    pais = models.CharField(max_length=200)
    departamento= models.CharField(max_length=200)
    municipio= models.CharField(max_length=200)
    