from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
 
# Create your models here.
director='director'
investigador = 'investigador'
curador= 'curador'
monitor='monitor'

grupos = ((director, 'Director'), (investigador, 'Investigador'), (curador, 'Curador'), (monitor, 'Monitor'))

class Usuario(User):
    identificacion= models.IntegerField()
    rol=models.CharField(max_length=10, choices=grupos, default='monitor')
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'Perfiles de Usuario'
    
    




