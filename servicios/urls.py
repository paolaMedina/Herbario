from django.urls import include, path
from . import views
# from .views import ServiciosList

app_name = 'servicios'
urlpatterns = [
    path(r'crear', views.RegistrarServicio, name='crear_servicio'),
    path(r'editar/<int:pk>', views.RegistrarServicio, name='editar_servicio'),
    path(r'procesar/<int:pk>', views.ProcesarServicio, name='procesar_servicio'),
    path(r'inicar/<int:pk>', views.CancelarServicio, name='cancelar_servicio'),
    path(r'entregar/<int:pk>', views.EntregarServicio, name='entregar_servicio'),
    path(r'terminar/<int:pk>', views.TerminarServicio, name='terminar_servicio'),
    path(r'listar', views.ListarServicio, name='listar_servicio'),
    # path(r'listar', ServiciosList.as_view(), name='listar_servicio'),

]
