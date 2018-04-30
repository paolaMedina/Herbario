from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add$', views.RegistrarEspecimen, name='crear_especimen'),
    url(r'nombres-autocomplete', views.autocomplete, name='ajax_autocomplete'),
    url(r'^listar', views.ListarEspecimen, name='listar_especimen'),
    url(r'^editar/(?P<pk>\d+)', views.RegistrarEspecimen, name='editar_especimen'),
    url(r'^eliminar/(?P<pk>\d+)', views.EliminarEspecimen, name='eliminar_especimen'),
    
]
