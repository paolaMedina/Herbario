from __future__ import unicode_literals

from django.db import models

# Create your models here.
from cientifico.models import Cientifico

class CategoriaTaxonomica (models.Model):
        familia = models.CharField(max_length=200)
        genero = models.CharField(max_length=200)
        epiteto_especifico = models.CharField(max_length=200)
        fecha_det = models.CharField(max_length=10)
        categoria_infraespecifica = models.CharField(max_length=200)
        epiteto_infraespecifico = models.CharField(max_length=200)
        autor1 = models.TextField()
        autor2 = models.TextField()


        
                