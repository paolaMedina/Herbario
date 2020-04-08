from django.urls import include, path
from . import views
# from .views import ServiciosList

app_name= 'prestamo'
urlpatterns = [
    path(r'solicitar', views.solicitudPrestamo, name='solicitar_prestamo'),
    # path(r'listar', ServiciosList.as_view(), name='listar_servicio'),

]