from django.db import models
from usuario.models import Usuario
from cliente.models import Cliente

# Create your models here.
type_services = (('cuarentena', 'Servicio de cuarentena'),('identificación', 'Servicio de identificación'))
state = (('solicitud', 'Solicitud'),('proceso','Proceso'),('terminado','Terminado'),('entregado','Entregado'),('cancelado','Cancelado'))


class Servicios (models.Model):
    ticket =  models.TextField()
    tipo = models.CharField(max_length=20, choices=type_services)
    descripcion = models.TextField()
    precio =  models.PositiveIntegerField()
    fecha_inicio = models.DateField(auto_now=True)
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=state)
    foto = models.ImageField(upload_to='servicios/', null=True, blank=True)
    encargado = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=None)