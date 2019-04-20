from django.conf.urls import url

from . import views
from .views import RegistroVisita,ListarVisitas,aprobar

urlpatterns = [
    
    url(r'^generar', RegistroVisita.as_view(), name='crear_visita'),
    url(r'^ver/(?P<pk>\d+)', views.view, name='detalle_visita'),
    url(r'^listar', ListarVisitas.as_view(), name='listar_visita'),
    url(r'^aprobar/(?P<pk>\d+)', views.aprobar, name='aprobar_visita'),
    # url(r'^deleteFile', views.EliminarArchivo, name='eliminar_archivo'),
]
