#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

type_identificacion=(('CC', 'cédula de ciudadanía'),('TP', 'tarjeta pasaporte'), ('CE','cédula de extranjería') )
class Cliente (models.Model):
    nombre_completo = models.CharField(max_length=100)
    tipo_identificacion = (models.CharField(max_length=20, choices=type_identificacion, default='CC'))
    identificacion = models.PositiveIntegerField()
    correo = models.EmailField()
    num_contacto = models.PositiveIntegerField()
    institucion = models.CharField(max_length=100, null=True, blank=True, default=None)


