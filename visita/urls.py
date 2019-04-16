from django.conf.urls import url

from . import views
from .views import RegistroVisita

urlpatterns = [
    
    url(r'^generar', RegistroVisita.as_view(), name='crear_visita'),
    # url(r'^editar/(?P<pk>\d+)', EditarNoticia.as_view(), name='editar_noticia'),
    # url(r'^listar', ListarNoticia.as_view(), name='listar_noticia'),
    # url(r'^eliminar/(?P<pk>\d+)', EliminarNoticia.as_view(), name='eliminar_noticia'),
    # url(r'^deleteFile', views.EliminarArchivo, name='eliminar_archivo'),
]
