
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
from noticia.models import Noticia
from visita.models import Visita
from especimen.models import Especimen
from servicios.models import Servicios


@login_required
def Dashboard(request):
    visitas_pendientes = Visita.objects.filter(aprobada=False).count()
    visitas_aprobadas = Visita.objects.filter(aprobada=True).count()
    especimenes = Especimen.objects.all().count()
    servicios_s = Servicios.objects.filter(estado='solicitud').count()
    servicios_p = Servicios.objects.filter(estado='proceso').count()
    servicios_t = Servicios.objects.filter(estado='terminado').count()
    servicios_e = Servicios.objects.filter(estado='entregado').count()
    servicios_c = Servicios.objects.filter(estado='cancelado').count()
    contexto = {'vsts_pndts': visitas_pendientes,'vsts_aprbds':visitas_aprobadas, 'especimenes':especimenes, 'servicios_s':servicios_s,
                'servicios_p':servicios_p, 'servicios_t':servicios_t, 'servicios_e':servicios_e, 'servicios_c':servicios_c}
    print (contexto)
    return render(request, 'index.html',contexto)


def Home(request):
    noticias = Noticia.objects.all()
    # print(noticias)
    contexto = {'noticias': noticias}
    return render(request, 'index-home.html', contexto)
