from django.db import models
from django.contrib.auth.models import User
from cliente.models import Cliente

# Create your models here.
type_services = (('identificación', 'Servicio de identificación'),('cuarentena', 'Servicio de cuarentena'),('secado', 'Servicio de secado'))
state = (('solicitud', 'Solicitud'),('proceso','Proceso'),('terminado','Terminado'),('entregado','Entregado'),('cancelado','Cancelado'))


class Servicios (models.Model):
    ticket = models.TextField()
    tipo = models.CharField(max_length=20, choices=type_services)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    fecha_inicio = models.DateField(auto_now=True)
    fecha_fin = models.DateField(null=True, blank=True, default=None)
    estado = models.CharField(max_length=20, choices=state, default='solicitud')
    foto = models.ImageField(upload_to='servicios/', null=True, blank=True)
    encargado = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=None)