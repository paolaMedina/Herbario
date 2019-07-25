from django.urls import include, path
from . import views
from .views import *
app_name = 'visita'
urlpatterns = [

    path(r'generar', RegistroVisita.as_view(), name='crear_visita'),
    path(r'ver/<int:pk>', views.view, name='detalle_visita'),
    path(r'listar', ListarVisitas.as_view(), name='listar_visita'),
    path(r'aprobar/<int:pk>', views.aprobar, name='aprobar_visita'),
    path(r'envioCorreo', views.envioCorreo, name='envio_correo'),
    # path(r'deleteFile', views.EliminarArchivo, name='eliminar_archivo'),
]
