from django.shortcuts import render
from .models import Prestamo
from .forms import SolicitudForm
from cliente.forms import ClienteForm

# Create your views here.



def solicitudPrestamo(request) : 
    solicitudForm = SolicitudForm()
    formCliente = ClienteForm()
    return render(request, 'solicitud.html', { 'solicitudForm':solicitudForm, 'formCliente':formCliente})
