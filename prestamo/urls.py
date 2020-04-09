from django.urls import include, path
from . import views
# from .views import ServiciosList

app_name= 'prestamo'
urlpatterns = [
    path(r'solicitar', views.solicitudPrestamo, name='solicitar_prestamo'),
    path(r'registrar', views.realizarPrestamo, name='realizar_prestamo'),
    path(r'listar/solicitudes', views.listarSolicitudes, name='listar_solicitud'),
    path(r'listar/prestamos', views.listarPrestamos, name='listar_prestamo'),
    # path(r'listar', ServiciosList.as_view(), name='listar_servicio'),

]