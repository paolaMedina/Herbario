from django.db import models

class Cliente (models.Model):
    nombre_completo = models.CharField(max_length=100)
    identificacion = models.IntegerField()
    correo = models.EmailField()
    institucion = models.CharField(max_length=100, null=True, blank=True)


