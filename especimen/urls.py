from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^crear', views.RegistrarEspecimen, name='crear_especimen'),
    url(r'nombres-autocomplete', views.autocomplete, name='ajax_autocomplete'),
    url(r'^listar', views.ListarEspecimen, name='listar_especimen'),
    url(r'^mi_lista', views.ListarEspecimenesPersonales, name='listar_personal'),
    url(r'^editar/(?P<pk>\d+)', views.RegistrarEspecimen, name='editar_especimen'),
    url(r'^eliminar/(?P<pk>\d+)', views.EliminarEspecimen, name='eliminar_especimen'),
    url(r'^update/(?P<pk>\d+)', views.ChangeEspecimen, name='cambiar_especimen'),
    url(r'^update', views.ChangeEspecimen, name='actualizar_especimen'),
    url(r'^busqueda', views.searchEspecimen, name='testing'),
    url(r'^api/get_especimenes', views.autocompleteFilter, name='autocompleteEspecimen'),
    url(r'^api/busqueda', views.busquedaAvanzada, name='busquedaAvanzada'),
    url(r'^detalle/(?P<pk>\d+)', views.vistaEspecimen, name='vistaEspecimen'),
    url(r'^colectores', views.busquedaColectores, name='busquedaColectores')
]
