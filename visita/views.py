# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.http.response import HttpResponseRedirect
from smtplib import SMTPException
from datetime import datetime
from herbario1.utilities import *
import config
from .models import Visita
from .forms import VisitaForm
import json  
from django.http import JsonResponse



def getEvents(request):
    queryset = Visita.objects.filter(aprobada=True)
    # print  (queryset)
    lista = []       
    for i in queryset:
        lista.append({'nombre' : i.nombre, 'fecha' : i.fecha, ' hora' : i.hora})
    data = {
        'lista': lista,
    }
    return JsonResponse(data) 	

class RegistroVisita(CreateView):
    template_name = "crearVisita.html"
    success_url = reverse_lazy("visita:crear_visita")
    model = Visita
    form_class = VisitaForm

    def form_valid(self, form):

        form.save()
        email_subject = 'Solicitud de visita'
        url = config.url+'/visita/listar '
        email_body = "El usuario %s acaba de realizar una solicitud de visita al herbario para el día  %s. \n por favor realiza la confirmación de este evento lo mas pronto posible aqui: %s." % (
            form.cleaned_data['nombre'], form.cleaned_data['fecha'], url)

        # envio de correo a encargados del herbario para ifnromarle nuevas visitas pendientes por aprobar
        send_mail(email_subject, email_body, config.email_herbario,
                  [config.email_herbario], fail_silently=False)

        return super(RegistroVisita, self).form_valid(form)

    def form_invalid(self, form):
        print(form['hora'])
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
        visita.save()
        messages.success(request, 'Visita agendada')
    except Visita.DoesNotExist:
        messages.error(request, 'No existe visita')

    return HttpResponseRedirect(reverse_lazy("visita:listar_visita"))


def actualizarVisita(request):
    if request.is_ajax():
        id_visita = request.GET.get('id', None)
        try:
            visita = Visita.objects.get(pk=id_visita)
            hora_request = request.GET.get('hora', None)
            fecha_request = request.GET.get('fecha', None)
            # print(visita.hora != hora_request)
            # print(visita.hora.strftime("%H:%M"))
            visita.fecha = visita.fecha.strftime("%Y-%m-%d")
            visita.hora = visita.hora.strftime("%H:%M")
            # print (visita.fecha == fecha_request)
            if(visita.hora != hora_request or visita.fecha != fecha_request):
                # print ('diferente')
                visita.hora = request.GET.get('hora', None)
                visita.fecha = request.GET.get('fecha', None)

                #envio de correo notificando cambio
                email = {
                    'body' : 'Hemos reagendado tu visita al herbario CUVC, te esperamos para que aprendas mas de nostros',
                    'subject' : 'Reagendamiento de visita',
                    'address' : visita.correo
                }
            else:
                # print('igual')
                email = {
                    'body' : 'Te esperamos para que aprendas mas de nostros',
                    'subject' : 'Aceptación de visita',
                    'address' : visita.correo
                }
            correo(email)
            visita.aprobada = True
            visita.save()
            output = {'type':'200', 'message':'Se modifico el horario de la visita y se le notifico al solicitante'}
        except Visita.DoesNotExist:
            output = {'type':'404', 'message':'visita no encontrada'}

    return JsonResponse(output) 	
    

@verificar_rol(roles_permitidos=["curador", "director"])
def view(request, pk):
    try:
        visita = Visita.objects.get(pk=pk)
        print(visita)
        return render(request, 'detalleVisita.html', {'visita': visita})

    except Visita.DoesNotExist:
        messages.error(request, 'No existe visita')
        return HttpResponseRedirect(reverse_lazy("visita:listar_visita"))


@verificar_rol(roles_permitidos=["curador", "director","investigador"])
def viewCalendar(request):

    return render(request, 'calendario.html')


def envioCorreo(request):
    email_body = request.POST.get('mensaje', None)
    email_subject = 'Agendamiento de visita Herbario CUVC'

    try:
        send_mail(email_subject, email_body, config.email_herbario,
                  [request.POST.get('correo', None)], fail_silently=False)
        messages.success(request, 'Se envio el correo satisfactoriamente')
    except SMTPException as e:
        messages.error(request, 'error al enviar el correo')
        print('There was an error sending an email: ', e)

    return HttpResponseRedirect(reverse_lazy("visita:listar_visita"))


def correo(input):
    email_body = input['body']
    email_subject = input['subject']
    email_address = input['address']

    try:
        send_mail(email_subject, email_body, config.email_herbario, [email_address], fail_silently=False)
        output = {'type':'200', 'message':'Se envio el correo satisfactoriamente'}
        print('correo enviado')

    except SMTPException as e:
        output = {'type':'404', 'message':'error al enviar el correo'}
        print('There was an error sending an email: ', e)

    return JsonResponse(output) 