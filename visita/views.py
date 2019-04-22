# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Visita
from herbario1.utilities import *
from .forms import VisitaForm
from django.http.response import HttpResponseRedirect


class RegistroVisita(CreateView):
    template_name = "crearVisita.html"
    success_url=reverse_lazy("visita:crear_visita")
    model = Visita
    form_class = VisitaForm

    def form_valid(self, form):
        form.save()
        return  super(RegistroVisita, self).form_valid(form)

    def form_invalid(self, form):
        error='hay uno o mas campos invalidos. Por favor verifique de nuevo'
        errorDjango=form.errors
        # messages.error(self.request,error )
        print (errorDjango)
        return  super(RegistroVisita, self).form_invalid(form)
        
class ListarVisitas(ListView):
    @verificar_rol(roles_permitidos=["director"])
    def dispatch(self, request, *args, **kwargs):
        return super(ListarVisitas, self).dispatch(request, *args, **kwargs)
        
    model=Visita
    template_name='listaVisita.html'
    queryset = Visita.objects.filter(aprobada=False)

@verificar_rol(roles_permitidos=["curador", "director"])
def aprobar(request,pk):
    try:
        visita= Visita.objects.get(pk=pk)
        visita.aprobada=True
        print (visita)
        visita.save()  
        messages.success(request, 'Visita agendada')
    except Visita.DoesNotExist:
        messages.error(request, 'No existe visita')
    
    return HttpResponseRedirect(reverse_lazy("visita:listar_visita"))

@verificar_rol(roles_permitidos=["curador", "director"])
def view(request, pk):
    try:
        visita= Visita.objects.get(pk=pk)
        print (visita)
        return render(request,'detalleVisita.html',{'visita':visita})

    except Visita.DoesNotExist:
        messages.error(request, 'No existe visita')
        return HttpResponseRedirect(reverse_lazy("visita:listar_visita"))


        
    
        


    