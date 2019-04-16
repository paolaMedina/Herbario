# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Visita
from .forms import VisitaForm


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
        print errorDjango
        return  super(RegistroVisita, self).form_invalid(form)
        
