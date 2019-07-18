# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.http.response import HttpResponseRedirect
from datetime import datetime
from herbario1.utilities import *
import config
from .models import Visita
from .forms import VisitaForm


class RegistroVisita(CreateView):
    template_name = "crearVisita.html"
    success_url = reverse_lazy("visita:crear_visita")
    model = Visita
    form_class = VisitaForm

    def form_valid(self, form):

        form.save()
        email_subject = 'Solicitud de visita'
        print(config.email_herbario)
        url = config.url+'/visita/listar '
        email_body = "El usuario %s acaba de realizar una solicitud de visita al herbario para el día  %s. \n por favor realiza la confirmación de este evento lo mas pronto posible aqui: %s." % (
            form.cleaned_data['nombre'], form.cleaned_data['fecha'], url)

        # envio de correo a encargados del herbario para ifnromarle nuevas visitas pendientes por aprobar
        send_mail(email_subject, email_body, config.email_herbario,
                  [config.email_herbario], fail_silently=False)

        return super(RegistroVisita, self).form_valid(form)

    def form_invalid(self, form):
        print(form['fecha'])
        error = 'hay uno o mas campos invalidos. Por favor verifique de nuevo'
        errorDjango = form.errors
        messages.error(self.request, error)
        print('jjj')
        print(errorDjango)
        return super(RegistroVisita, self).form_invalid(form)


class ListarVisitas(ListView):
    @verificar_rol(roles_permitidos=["director"])
    def dispatch(self, request, *args, **kwargs):
        return super(ListarVisitas, self).dispatch(request, *args, **kwargs)

    model = Visita
    template_name = 'listaVisita.html'
    queryset = Visita.objects.filter(aprobada=False)


@verificar_rol(roles_permitidos=["curador", "director"])
def aprobar(request, pk):
    try:
        visita = Visita.objects.get(pk=pk)
        visita.aprobada = True
        print(visita)
        visita.save()
        messages.success(request, 'Visita agendada')
    except Visita.DoesNotExist:
        messages.error(request, 'No existe visita')

    return HttpResponseRedirect(reverse_lazy("visita:listar_visita"))


@verificar_rol(roles_permitidos=["curador", "director"])
def view(request, pk):
    try:
        visita = Visita.objects.get(pk=pk)
        print(visita)
        return render(request, 'detalleVisita.html', {'visita': visita})

    except Visita.DoesNotExist:
        messages.error(request, 'No existe visita')
        return HttpResponseRedirect(reverse_lazy("visita:listar_visita"))
