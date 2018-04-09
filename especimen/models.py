from __future__ import unicode_literals

from django.db import models
from categoriaTaxonomica.models import CategoriaTaxonomica
from coleccion.models import Coleccion
from cientifico.models import Cientifico


# Create your models here.
BOOL_CHOICES = ((True, 'Si'), (False, 'No'))
extinta='EX'
peligro ='EP'
vulnerable = 'VU'
fuera_peligro = 'FP'

DANGER_CHOICES = ((extinta, 'Extinta'), (peligro, 'En Peligro'), (vulnerable, 'Vulnerable'), (fuera_peligro, 'Fuera de Peligro'))

class Especimen (models.Model):
    num_registro = models.PositiveIntegerField()
    categoria = models.ForeignKey(CategoriaTaxonomica, null=False, blank=False, on_delete=models.CASCADE)
    coleccion = models.ForeignKey(Coleccion, null=False, blank=False, on_delete=models.CASCADE)
    determinador = models.ForeignKey(Cientifico, null=False, blank=False, on_delete=models.CASCADE)
    #duplicado =  models.BooleanField(choices=BOOL_CHOICES)
    lugar_duplicado = models.CharField(max_length=200)
    #peligro = models.CharField(max_length=2, choices=DANGER_CHOICES)
    imagen = models.ImageField(upload_to='imagen_especimen', null=True, blank=True)
   #id usuario-id geografico