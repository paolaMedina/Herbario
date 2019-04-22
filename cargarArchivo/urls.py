from django.urls import include, path
from . import views

app_name = 'archivo'
urlpatterns = [
    path(r'upload', views.UploadFileView.as_view(), name='upload'),
]