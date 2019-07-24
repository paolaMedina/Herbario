"""herbario1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  path(r'^blog/', include(blog_urls))
"""
# from django.conf.urls import url, include
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import Dashboard
from .views import Home
from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth.views import LoginView


urlpatterns = [
    path(r'admin', admin.site.urls),
    path(r'', Home, name='inicio'),  
    path(r'dashboard', Dashboard, name = 'dashboard'),
    path(r'especimen/', include('especimen.urls')), 
    path(r'usuario/', include('usuario.urls')),
    path(r'archivo/', include('cargarArchivo.urls')),
    path(r'noticia/', include('noticia.urls')),
    path(r'visita/', include('visita.urls')),
    path(r'servicios/', include('servicios.urls')),
    path(r'password_reset',auth_views.PasswordResetView.as_view(template_name = 'password_reset.html',
    email_template_name ='password_reset_email.html'),name="password_reset"),
    
    path(r'password_reset/done',auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'),name="password_reset_done"),
   
    path(r'reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'),name="password_reset_confirm"), 

    path(r'reset/done',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name="password_reset_complete"),
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #url permite acceder a las imagenes de la carpeta media
