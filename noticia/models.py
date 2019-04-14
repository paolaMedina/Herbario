# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Noticia (models.Model):
    titulo = models.CharField(max_length=100)
    resumen = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='noticias/', null=True, blank=True)
