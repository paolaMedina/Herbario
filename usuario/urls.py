from django.urls import include, path
# from django.contrib.auth.views import logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib.auth import views as auth_views
from . import views


app_name = 'usuario'
urlpatterns = [
    path(r'registrar', login_required(
        RegistroUsuario.as_view()), name='registrar_usuario'),
    path(r'editar/<int:pk>', login_required(EditarUsuario.as_view()),
         name='editar_usuario'),
    path(r'listar', login_required(
        ListarUsuarios.as_view()), name='listar_usuario'),
    path(r'listar_inactivos', login_required(ListarUsuariosInactivos.as_view()),
         name='listar_usuario_inactivos'),
    path(r'monitores', views.ListarMonitores, name='listar_monitores'),
    # path(r'eliminar/(?P<pk>\d+)', EliminarUsuario.as_view(), name='eliminar_usuario'),
    path(r'eliminar/<int:pk>', views.EliminarUsuario, name='eliminar_usuario'),
    path(r'activar/<int:pk>', views.ActivarUsuario, name='activar_usuario'),
    # path(r'$', Login.as_view(), name="login"),
    path(r'', views.Login, name="login"),
    # kwargs={'next_page': '/'} ->redirecciona a la url raiz
    path(r'salir', auth_views.LogoutView.as_view(next_page='/'), name="salir"),

]
