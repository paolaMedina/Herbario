#Importamos la vista generica FormView
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .forms import RegistroForm,FormularioLogin
from .models import Usuario
from django.contrib.auth.models import Group

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class RegistroUsuario(LoginRequiredMixin,CreateView):
    model = Usuario
    form_class = RegistroForm
    template_name = "registrar.html"
    success_url=reverse_lazy("usuario:registrar_usuario")

    
    def form_valid(self, form):
        usuario= form.instance
        contra= usuario.first_name[0]
        print contra
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
        
         
class ListarUsuarios(LoginRequiredMixin,ListView):
    model=Usuario
    template_name='listar.html'
    

class EditarUsuario(LoginRequiredMixin,UpdateView):
     model = Usuario
     form_class = RegistroForm
     template_name = "registrar.html"
     success_url=reverse_lazy("usuario:registrar_usuario")
  
  
class EliminarUsuario(LoginRequiredMixin,DeleteView):
    model = Usuario
    success_url=reverse_lazy("usuario:listar_usuario")
    #funcion para no ingresar template de confirmacion delete
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        
        
        
        
        

class Login(FormView):
    #Establecemos la plantilla a utilizar
    template_name = 'login.html'
    #Le indicamos que el formulario a utilizar es el formulario de autenticacion de Django
    form_class = FormularioLogin 
    success_url =  reverse_lazy("dashboard")
 
    def dispatch(self, request, *args, **kwargs):
        #Si el usuario esta autenticado entonces nos direcciona a la url establecida en success_url
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        #Sino lo esta entonces nos muestra la plantilla del login simplemente
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)
 
    def form_valid(self, form):
        login(self.request, form.get_user())
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        return super(Login, self).form_valid(form)