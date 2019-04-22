from django.urls import include, path
# from django.contrib.auth.views import logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from .views import RegistroUsuario, EditarUsuario,ListarMonitores,EliminarUsuario, Login, ListarUsuarios
from django.contrib.auth import views as auth_views
from . import views


app_name = 'usuario'
urlpatterns = [
    path(r'registrar', RegistroUsuario.as_view(), name='registrar_usuario'),
    path(r'editar/<int:pk>', EditarUsuario.as_view(), name='editar_usuario'),
    path(r'listar', ListarUsuarios.as_view(), name='listar_usuario'),
    path(r'monitores',views.ListarMonitores, name='listar_monitores'),
    # path(r'eliminar/(?P<pk>\d+)', EliminarUsuario.as_view(), name='eliminar_usuario'),
    path(r'eliminar/<int:pk>', views.EliminarUsuario, name='eliminar_usuario'),
    # path(r'$', Login.as_view(), name="login"),
    path(r'', views.Login, name="login"),
    #kwargs={'next_page': '/'} ->redirecciona a la url raiz  
    path(r'salir', auth_views.LogoutView.as_view(next_page = '/'), name="salir"),
    
    ]    
     
     