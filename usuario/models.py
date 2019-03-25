from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
 
# Create your models here.
director='director'
investigador='investigador'
curador= 'curador'
monitor='monitor'

grupos = ((monitor, 'Monitor'),(investigador, 'Investigador'), (curador, 'Curador'), (director, 'Director'))


class Usuario(User):
    identificacion= models.IntegerField()
    rol=models.CharField(max_length=12, choices=grupos, default='monitor')
    # active=models.BooleanField(default=True)

    
    




