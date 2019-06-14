from django.urls import include, path
from . import views

app_name= 'servicios'
urlpatterns = [
    path(r'crear', views.RegistrarEspecimen, name='crear_especimen'),

]