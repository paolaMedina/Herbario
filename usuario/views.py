from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from .forms import RegistroForm
from .models import Usuario
from django.contrib.auth.models import Group

# Create your views here.

class RegistroUsuario(CreateView):
    model = Usuario
    form_class = RegistroForm
    template_name = "registrar.html"
    success_url=reverse_lazy("usuario:registrar_usuario")
    
    
    def form_valid(self, form):
        usuario= form.instance
        self.object = form.save()
        if (usuario.rol=='director'):
            grupo_director, grupo_director_creado = Group.objects.get_or_create(name='Director')
            grupo_director.user_set.add(self.object)
        elif (usuario.rol=='investigador'):
            grupo_investigador, grupo_investigador_creado = Group.objects.get_or_create(name='Investigador')
            grupo_investigador.user_set.add(self.object)
        elif (usuario.rol=='curador'):
            grupo_curador, grupo_curador_creado = Group.objects.get_or_create(name='Curador')
            grupo_curador.user_set.add(self.object)
        else:
            grupo_monitor, grupo_monitor_creado = Group.objects.get_or_create(name='Monitor')
            grupo_monitor.user_set.add(self.object)
        
        messages.success(self.request, 'Se agrego el usuario con EXITO')
        print "exito"
        return super(RegistroUsuario, self).form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'hay uno o mas campos invalidos. Por favor verifique de nuevo')
        print "malo"
        return  super(RegistroUsuario, self).form_invalid(form)