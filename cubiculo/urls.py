from django.urls import include, path
from . import views
# from .views import ServiciosList

app_name = 'cubiculo'
urlpatterns = [
    path(r'crear', views.SolcitudCubiculo, name='crear_cubiculo'),
    path(r'listar_cubiculo', views.listarCubiculo, name='listar_cubiculo'),
    path(r'listar_solicitudes', views.ListarSolicitud, name='listar_solicitud')
]
