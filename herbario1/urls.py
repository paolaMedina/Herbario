"""herbario1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import Dashboard
from .views import Home
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home, name='inicio'),  
    url(r'^dashboard', Dashboard, name = 'dashboard'),
    url(r'^especimen/', include('especimen.urls', namespace = 'especimen')), 
    url(r'^usuario/', include('usuario.urls', namespace = 'usuario')),
    url(r'^archivo/', include('cargarArchivo.urls', namespace = 'archivo')),
    url(r'^reset/password_reset/$',password_reset,{'template_name':'password_reset.html',
    'email_template_name':'password_reset_email.html'},name="password_reset"),
    url(r'^password_reset_done/$', password_reset_done, {'template_name':'password_reset_done.html'},name="password_reset_done"),
   
    url(r'^reset/(?P<uidb64>[0-94-Za-z_\-]+)/(?P<token>.+)/$',password_reset_confirm,{'template_name':'password_reset_confirm.html'},name="password_reset_confirm"), 
    url(r'^reset/done',password_reset_complete,{'template_name':'password_reset_complete.html'},name="password_reset_complete"),
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #url permite acceder a las imagenes de la carpeta media
