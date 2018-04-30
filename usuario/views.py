from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from .forms import RegistroForm

# Create your views here.

class RegistroUsuario(CreateView):
    model = User
    template_name = "registrar.html"
    form_class = RegistroForm
    success_url=reverse_lazy("usuario:registrar_usuario")
    
    def form_valid(self, form):
        messages.success(self.request, messages.SUCCESS, 'Se agrego el usuario con EXITO')
        print "exito"
        return super(RegistroUsuario, self).form_valid(form)
    
    def form_invalid(self, form):
        response = super(RegistroUsuario, self).form_invalid(form)
        messages.error(self.request, 'hay uno o mas campos invalidos. Por favor verifique de nuevo')
        print "malo"
        return response