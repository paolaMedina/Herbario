from __future__ import unicode_literals

from django.db import models

from cientifico.models import Cientifico

# Create your models here.
class Coleccion(models.Model):
    colector_ppal = models.ForeignKey(Cientifico, null=False, blank=False, on_delete=models.CASCADE,related_name="principal")
    fecha = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=200)
    colectores_secu =models.ManyToManyField(Cientifico, through='Colectores', null=True, blank=True)

#relacion muchos a muchos de coleccion y cientifico, con atributo adicional, que indica en orden de relevancia 
class Colectores(models.Model):
    coleccion =  models.ForeignKey(Coleccion, on_delete=models.CASCADE)
    colector = models.ForeignKey(Cientifico, on_delete=models.CASCADE)
    orden = models.IntegerField()
    unique_together  = ("coleccion", "colector")
   
