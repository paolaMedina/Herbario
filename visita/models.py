# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Visita (models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    nombre = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.IntegerField()
    numPersonas = models.IntegerField()
    motivo = models.TextField()
    aprobada = models.BooleanField(default=False)