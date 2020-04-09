from django.urls import include, path
from . import views
# from .views import ServiciosList

app_name= 'prestamo'
urlpatterns = [
    path(r'solicitar', views.solicitudPrestamo, name='solicitar_prestamo'),
    path(r'registrar/<int:pk>', views.realizarPrestamo, name='realizar_prestamo'),
    path(r'listar/solicitudes', views.listarSolicitudes, name='listar_solicitud'),
    path(r'listar/prestamos', views.listarPrestamos, name='listar_prestamo'),
    path(r'solicitudes/cancelar/<int:pk>', views.cancelarSolicitud, name='cancelar_solicitud'),
    path(r'renovar/<int:pk>', views.renovar_prestamo, name='renovar_prestamo'),
    path(r'regresar/<int:pk>', views.entregar_prestamo, name='regresar_prestamo'),
    # path(r'listar', ServiciosList.as_view(), name='listar_servicio'),

]