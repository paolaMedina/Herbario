from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^crear', views.RegistrarEspecimen, name='crear_especimen'),
    url(r'nombres-autocomplete', views.autocomplete, name='ajax_autocomplete'),
    url(r'^listar', views.ListarEspecimen, name='listar_especimen'),
    url(r'^editar/(?P<pk>\d+)', views.RegistrarEspecimen, name='editar_especimen'),
    url(r'^eliminar/(?P<pk>\d+)', views.EliminarEspecimen, name='eliminar_especimen'),
    url(r'^update/(?P<pk>\d+)', views.ChangeEspecimen, name='cambiar_especimen'),
    url(r'^update', views.ChangeEspecimen, name='actualizar_especimen'),
    url(r'^testing/$', views.searchEspecimen, name='testing'),
    url(r'^api/get_especimenes', views.autocompleteFilter, name='autocompleteEspecimen'),
    url(r'^api/busqueda', views.busquedaAvanzada, name='busqueda'),
    
    
]
