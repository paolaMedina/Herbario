#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from categoriaTaxonomica.models import CategoriaTaxonomica
from coleccion.models import Coleccion
from cientifico.models import Cientifico
from ubicacion.models import Ubicacion



# Create your models here.
extinto ='EX'
peligroCritico ='CR'
peligro ='EN'
vulnerable = 'VU'
casiAmenazado = 'NT'
preocupacionMenor = 'LC'
datosInsuficientes = 'DD'
noEvaluado = 'NE'

DANGER_CHOICES = ((extinto, 'Extinto'),(peligroCritico, 'En peligro crítico') ,(peligro, 'En Peligro'), (vulnerable, 'Vulnerable'), (casiAmenazado, 'Casi amenazado'), (preocupacionMenor, 'Preocupación Menor'), (datosInsuficientes, 'Datos insuficientes'), (noEvaluado, 'No evaluado'))

TYPE_CHOICES = (('holo', 'Holotipo'), ('iso', 'Isotipo'), ('lecto', 'Lectotipo'), ('isol', 'Isolectotipo'),('holol', 'Hololectotipo'))

class Especimen (models.Model):
    num_registro = models.PositiveIntegerField()
    categoria = models.ForeignKey(CategoriaTaxonomica, null=False, blank=False, on_delete=models.CASCADE)
    coleccion = models.ForeignKey(Coleccion, null=False, blank=False, on_delete=models.CASCADE)
    determinador = models.ForeignKey(Cientifico, null=False, blank=False, on_delete=models.CASCADE)
    lugar_duplicado = models.CharField(max_length=200)
    peligro = models.CharField(max_length=2, choices=DANGER_CHOICES, default='LC')
    imagen = models.ImageField(upload_to='fotografias/', null=True, blank=True)
    visible= models.BooleanField(default=True)
    tipo=models.CharField(max_length=5, choices=TYPE_CHOICES, default='holo')
    ubicacion = models.ForeignKey(Ubicacion, null=True, blank=True, on_delete=models.CASCADE)
   #id usuario