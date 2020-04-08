from django.db import models
from django.contrib.auth.models import User
from cliente.models import Cliente 

state = (('solicitud', 'Solicitud'),('prestamo','Prestamo'),('entregado','Entregado'))


class Prestamo (models.Model):
    solicitud = models.TextField()
    num_registro = models.PositiveIntegerField()
    fecha_entrega= models.DateField(auto_now=True)
    fecha_devolucion = models.DateField(null=True, blank=True, default=None)
    estado = models.CharField(max_length=20, choices=state, default='solicitud')
    observaciones_entrega = models.TextField()
    encargado = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=None)