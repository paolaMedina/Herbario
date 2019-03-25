from django.conf.urls import url, include
from django.contrib.auth.views import logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from .views import RegistroUsuario, EditarUsuario,ListarMonitores,EliminarUsuario, Login, ListarUsuarios
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^registrar', RegistroUsuario.as_view(), name='registrar_usuario'),
    url(r'^editar/(?P<pk>\d+)', EditarUsuario.as_view(), name='editar_usuario'),
    url(r'^listar', ListarUsuarios.as_view(), name='listar_usuario'),
    url(r'^monitores',views.ListarMonitores, name='listar_monitores'),
    # url(r'^eliminar/(?P<pk>\d+)', EliminarUsuario.as_view(), name='eliminar_usuario'),
    url(r'^eliminar/(?P<pk>\d+)', views.EliminarUsuario, name='eliminar_usuario'),
    # url(r'^$', Login.as_view(), name="login"),
    url(r'^$', views.Login, name="login"),
    #kwargs={'next_page': '/'} ->redirecciona a la url raiz  
    url(r'^salir$', logout, name="salir", kwargs={'next_page': '/'}),
    
    ]    
     
     