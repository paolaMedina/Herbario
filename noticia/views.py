# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Noticia
from .forms import NoticiaForm
from django.contrib.messages.views import SuccessMessageMixin
import json
from django.http import HttpResponse
from herbario1.utilities import *

# Create your views here.

class RegistroNoticia(CreateView):
    template_name = "createNoticia.html"
    success_url=reverse_lazy("noticia:listar_noticia")
    model = Noticia
    form_class = NoticiaForm
    
    # # @verificar_rol(roles_permitidos=["curador", "director"])
    # # def dispatch(self, request, *args, **kwargs):
    # #     return super(RegistroNoticia, self).dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        form.save()
        messages.success(self.request,'Noticia guardada')
        return  super(RegistroNoticia, self).form_valid(form)

    def form_invalid(self, form):
        error='hay uno o mas campos invalidos. Por favor verifique de nuevo'
        errorDjango=form.errors
        messages.error(self.request,error )
        print errorDjango
        return  super(RegistroNoticia, self).form_invalid(form)
        
class EditarNoticia(UpdateView):
    # @verificar_rol(roles_permitidos=["curador", "director"])
    # def dispatch(self, request, *args, **kwargs):
    #     return super(EditarNoticia, self).dispatch(request, *args, **kwargs)
    model = Noticia
    form_class = NoticiaForm
    success_message = 'Noticia actualizada'
    template_name = "createNoticia.html"
    success_url=reverse_lazy("noticia:listar_noticia")


class EliminarNoticia(DeleteView):
    
    # @verificar_rol(roles_permitidos=["curador", "director"])
    # def dispatch(self, request, *args, **kwargs):
    #     return super(EliminarNoticia, self).dispatch(request, *args, **kwargs)
        
    model = Noticia
    success_url=reverse_lazy("noticia:listar_noticia")
    success_message = 'Se elimino la noticia con EXITO'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        #borrar fisicamente el archivo
        noticia = Noticia.objects.get(id=kwargs['pk'])
        imagen=noticia.imagen
        file_path = settings.MEDIA_ROOT+'/' + str(imagen)
        os.remove(file_path)
        return super(EliminarNoticia, self).delete(request, *args, **kwargs) 
        
    #funcion para no ingresar template de confirmacion delete
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class ListarNoticia(ListView):
    # @verificar_rol(roles_permitidos=["curador", "director"])
    # def dispatch(self, request, *args, **kwargs):
    #     return super(ListarNoticia, self).dispatch(request, *args, **kwargs)
    model=Noticia
    template_name='listarNoticia.html'

def  EliminarArchivo():
    print 'aqui'
    return HttpResponse(json.dumps({}), content_type="application/json")
