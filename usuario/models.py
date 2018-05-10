from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
director='director'
investigador = 'investigador'
curador= 'curador'
monitor='monitor'

grupos = ((director, 'Director'), (investigador, 'Investigador'), (curador, 'Curador'), (monitor, 'Monitor'))

class Usuario(User):
    identificacion= models.IntegerField()
    rol=models.CharField(max_length=10, choices=grupos, default='monitor')
    
    




