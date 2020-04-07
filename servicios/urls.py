from django.urls import include, path
from . import views
# from .views import ServiciosList

app_name = 'servicios'
urlpatterns = [
    path(r'crear', views.RegistrarServicio, name='crear_servicio'),
    path(r'editar/<int:pk>', views.RegistrarServicio, name='editar_servicio'),
    path(r'listar', views.ListarServicio, name='listar_servicio'),
    # path(r'listar', ServiciosList.as_view(), name='listar_servicio'),

]
