#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Importamos la vista generica FormView
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import render,get_object_or_404, render_to_response
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
import hashlib, datetime, random
from django.utils import timezone
from .forms import RegistroForm,FormularioLogin
from .models import Usuario
from herbario1.utilities import *
from django.contrib.auth.decorators  import  login_required
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth import authenticate

class RegistroUsuario(CreateView):
    template_name = "registrar.html"
    success_url=reverse_lazy("usuario:registrar_usuario")
    model = Usuario
    form_class = RegistroForm

    @verificar_rol(roles_permitidos=["curador", "director"])
    def dispatch(self, request, *args, **kwargs):
        return super(RegistroUsuario, self).dispatch(request, *args, **kwargs)
        
    # #se envia el grupo del usuario al formulario, para poder verificar si es un curador y hacer el respectivo cambio 
    def get_form_kwargs(self):
        kwargs = super(RegistroUsuario, self).get_form_kwargs()
        return dict(kwargs, groups= self.request.user.groups.values_list('name', flat=True))

    def form_valid(self, form):

        usuario= form.instance
        #contrasena con la inicial del nombre en mayuscula, la identificacion y la inicial del apellido en mayuscula
        contra= usuario.first_name[0].upper()+str(usuario.identificacion)+usuario.last_name[0].upper()
        usuario.password1=contra
        
        email = form.cleaned_data['email']
        # Enviar un email de confirmacion
        email_subject = 'Account confirmation'
        email_body = "Buenas acabas de ser registrado en la pagina del Herbario CUVC de la Universidad del valle. Tus datos de registro son: \n Usuario:%s \n contrasena es %s \n puedes ingresar al siguiente link para loguearte: https://herbario1-paolamedina.c9users.io/usuario/" % (usuario.username,usuario.password1)
        
        # send_mail(email_subject, email_body, 'angiepmc93@gmail.com',
        #     [email], fail_silently=False)
        
        self.object = form.save(commit=False)
        self.object.set_password(contra)
        self.object.save()
        
        #agrupar usuario depndiendo su rol
        if (usuario.rol=='director'):
            grupo_director, grupo_director_creado = Group.objects.get_or_create(name='director')
            grupo_director.user_set.add(self.object)
        elif (usuario.rol=='investigador'):
            grupo_investigador, grupo_investigador_creado = Group.objects.get_or_create(name='investigador')
            grupo_investigador.user_set.add(self.object)
        elif (usuario.rol=='curador'):
            grupo_curador, grupo_curador_creado = Group.objects.get_or_create(name='curador')
            grupo_curador.user_set.add(self.object)
        else:
            grupo_monitor, grupo_monitor_creado = Group.objects.get_or_create(name='monitor')
            grupo_monitor.user_set.add(self.object)
            
            
        messages.success(self.request, 'Se agrego el usuario con EXITO')
        return super(RegistroUsuario, self).form_valid(form)
    
    def form_invalid(self, form):

        error='hay uno o mas campos invalidos. Por favor verifique de nuevo'
        errorDjango=form.errors
        messages.error(self.request,error )
        print (errorDjango)
        return  super(RegistroUsuario, self).form_invalid(form)
        
class ListarUsuarios(ListView):
    # @verificar_rol(roles_permitidos=["director"])
    def dispatch(self, request, *args, **kwargs):
        return super(ListarUsuarios, self).dispatch(request, *args, **kwargs)
        
    model=Usuario
    template_name='listar.html'
    # queryset = Usuario.objects.filter(is_active=True)
    
@login_required
# @has_role_decorator(['curador'])
@verificar_rol(roles_permitidos=["curador"])
def ListarMonitores(request):
        
    # monitor= Usuario.objects.filter(rol='monitor', is_active=True)
    monitor= Usuario.objects.filter(rol='monitor')
    contexto = {'monitores':monitor}
    return render(request,'listarMonitores.html', contexto )
    
class EditarUsuario(SuccessMessageMixin,UpdateView):
    @verificar_rol(roles_permitidos=["curador", "director"])
    def dispatch(self, request, *args, **kwargs):
        return super(EditarUsuario, self).dispatch(request, *args, **kwargs)
        
        
    #se envia el grupo del usuario al formulario, para poder verificar si es un curador y hacer el respectivo cambio 
    def get_form_kwargs(self):
        kwargs = super(EditarUsuario, self).get_form_kwargs()
        groupUser=self.request.user.groups.values_list('name', flat=True)
        return dict(kwargs, groups=groupUser)
    model = Usuario
    form_class = RegistroForm
    success_message = 'Usuario actualizado'
    template_name = "registrar.html"
    success_url=reverse_lazy("dashboard")
  
# class EliminarUsuario(DeleteView):
    
#     @verificar_rol(roles_permitidos=["curador", "director"])
#     def dispatch(self, request, *args, **kwargs):
#         return super(EliminarUsuario, self).dispatch(request, *args, **kwargs)
        
#     model = Usuario
#     success_url=reverse_lazy("usuario:listar_usuario")
#     success_message = 'Se elimino el usuario con EXITO'
    
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super(EliminarUsuario, self).delete(request, *args, **kwargs) 
        
#     #funcion para no ingresar template de confirmacion delete
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)
        
def EliminarUsuario(request,pk):
    usuario= Usuario.objects.get(pk=pk)
    usuario.is_active=False
    usuario.save()  
    messages.success(request, 'Se elimino el usuario con EXITO')
    return HttpResponseRedirect(reverse_lazy("usuario:listar_usuario"))

# class Login(FormView):
#     # Establecemos la plantilla a utilizar
#     template_name = 'login.html'
#     #Le indicamos que el formulario a utilizar es el formulario de autenticacion de Django
#     form_class = FormularioLogin 
#     success_url =  reverse_lazy("dashboard")
 
#     def dispatch(self, request, *args, **kwargs):
#         #Si el usuario esta autenticado entonces nos direcciona a la url establecida en success_url
#         if request.user.is_authenticated():
#             return HttpResponseRedirect(self.get_success_url())
#         #Sino lo esta entonces nos muestra la plantilla del login simplemente
#         else:
#             return super(Login, self).dispatch(request, *args, **kwargs)
 
#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         return super(Login, self).form_valid(form)
    
#     def form_invalid(self, form):   
#         print self.request.user
#         if  self.request.user.is_active == False:
#             messages.error(self.request,'El usuario no esta activo')
#             return redirect('usuario:login')
#         else:
#             messages.error(self.request, 'El usuario o contraseña no coinciden o no existen')
#             return redirect('usuario:login')
def myAuthenticate( username=None, password=None):
    try:
        user = Usuario.objects.get(email=username)
        print (user)
        if user.check_password(password):
            return user
    except Usuario.DoesNotExist:
        try:
            user = Usuario.objects.get(username=username)
            print (user)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            return None

def Login(request):
    if request.method == 'POST':
        form = FormularioLogin(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user =  myAuthenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request,'El usuario no esta activo')
                return redirect('usuario:login')
        else:
            messages.error(request,'El usuario o contraseña no coinciden o no existen')
            return redirect('usuario:login')
    else:
        # Si el usuario esta autenticado entonces nos direcciona a la url establecida en success_url
        if request.user.is_authenticated:
            return redirect('dashboard')
        #Sino lo esta entonces nos muestra la plantilla del login simplemente
        else:
            form = FormularioLogin()
    return render(request, 'login.html', {'form': form})
