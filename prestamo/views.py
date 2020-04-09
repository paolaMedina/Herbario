from django.shortcuts import render
from .models import Prestamo
from .forms import SolicitudForm, PrestamoForm
from cliente.forms import ClienteForm


def solicitudPrestamo(request) : 
    solicitudForm = SolicitudForm()
    formCliente = ClienteForm()
    return render(request, 'solicitud.html', { 'solicitudForm':solicitudForm, 'formCliente':formCliente})

def realizarPrestamo(request):

    prestamoForm = PrestamoForm()
    formCliente = ClienteForm()
    return render(request, 'prestamo.html', { 'prestamoForm':prestamoForm, 'formCliente':formCliente})