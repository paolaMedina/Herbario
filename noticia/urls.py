from django.urls import include, path
from . import views
from .views import RegistroNoticia,EditarNoticia,ListarNoticia,EliminarNoticia,EliminarArchivo

app_name = 'noticia'
urlpatterns = [
    
    path(r'crear', RegistroNoticia.as_view(), name='crear_noticia'),
    path(r'editar/<int:pk>', EditarNoticia.as_view(), name='editar_noticia'),
    path(r'listar', ListarNoticia.as_view(), name='listar_noticia'),
    path(r'eliminar/<int:pk>', EliminarNoticia.as_view(), name='eliminar_noticia'),
    path(r'deleteFile', views.EliminarArchivo, name='eliminar_archivo'),
]
