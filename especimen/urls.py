from django.urls import include, path
from . import views

app_name= 'especimen'
urlpatterns = [
    path(r'crear', views.RegistrarEspecimen, name='crear_especimen'),
    path(r'nombres-autocomplete', views.autocomplete, name='ajax_autocomplete'),
    path(r'listar', views.ListarEspecimen, name='listar_especimen'),
    path(r'mi_lista', views.ListarEspecimenesPersonales, name='listar_personal'),
    path(r'editar/<int:pk>', views.RegistrarEspecimen, name='editar_especimen'),
    path(r'eliminar/<int:pk>', views.EliminarEspecimen, name='eliminar_especimen'),
    path(r'update/<int:pk>', views.ChangeEspecimen, name='cambiar_especimen'),
    path(r'update', views.ChangeEspecimen, name='actualizar_especimen'),
    path(r'busqueda', views.searchEspecimen, name='testing'),
    path(r'api/get_especimenes', views.autocompleteFilter, name='autocompleteEspecimen'),
    path(r'api/busqueda', views.busquedaAvanzada, name='busquedaAvanzada'),
    path(r'detalle/<int:pk>', views.vistaEspecimen, name='vistaEspecimen'),
    path(r'colectores', views.busquedaColectores, name='busquedaColectores')
]
