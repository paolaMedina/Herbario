#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from categoriaTaxonomica.models import CategoriaTaxonomica
from coleccion.models import Coleccion
from cientifico.models import Cientifico
from usuario.models import Usuario
from ubicacion.models import Ubicacion
from django.contrib.auth.models import User


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

TYPE_CHOICES = (('NoTipo', 'No tipo'),('Holotipo', 'Holotipo'), ('Isotipo', 'Isotipo'), ('Lectotipo', 'Lectotipo'), ('Isolectotipo', 'Isolectotipo'),('Hololectotipo', 'Hololectotipo'))

class Especimen (models.Model):
    num_registro = models.PositiveIntegerField()
    categoria = models.ForeignKey(CategoriaTaxonomica, null=True, blank=True, on_delete=models.CASCADE, default=None)
    coleccion = models.ForeignKey(Coleccion, null=True, blank=True, on_delete=models.CASCADE, default=None)
    determinador = models.ForeignKey(Cientifico, null=True, blank=True, on_delete=models.CASCADE, default=None)
    lugar_duplicado = models.CharField(max_length=200)
    peligro = models.CharField(max_length=2, choices=DANGER_CHOICES, default='LC')
    imagen = models.ImageField(upload_to='fotografias/', null=True, blank=True)
    visible= models.BooleanField(default=True)
    tipo=models.CharField(max_length=15, choices=TYPE_CHOICES, default='NoTipo')
    ubicacion = models.ForeignKey(Ubicacion, null=True, blank=True, on_delete=models.CASCADE,default=None)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, default=None)