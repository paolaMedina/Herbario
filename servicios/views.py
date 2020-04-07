from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators  import  login_required
from django.shortcuts import render, HttpResponseRedirect
from servicios.models import Servicios
from servicios.forms import ServiciosForm
from cliente.models import Cliente
from cliente.forms import ClienteForm
from uuid import uuid4
from herbario1.utilities import *
from django.views.generic import ListView

# Create your views here.
@login_required
def RegistrarServicio(request, pk=None):

    if pk:
        print(pk)
        try:
            servicio = Servicios.objects.get(pk=pk)
            cliente = Cliente.objects.get(pk=servicio.cliente.pk)
            mensaje_exito = "Se edito exitosamente"
        except  Servicios.DoesNotExist:
            messages.error(request, 'No existe el servicio en consulta')
            return HttpResponseRedirect(reverse_lazy('servicios:crear_servicio'))
    else:
        servicio = Servicios()
        cliente = Cliente()
        mensaje_exito = 'Se ha guardado exitosamente'
        # viewsRedirect='especimen:crear_especimen'

    if request.method == 'POST':
        print("solicitud post")
        
        formServicio = ServiciosForm(request.POST, request.FILES,instance=servicio)
        formCliente = ClienteForm(
            request.POST, request.FILES, instance=cliente)

        if formServicio.is_valid() and formCliente.is_valid():
            print("valido")
            try:
                cliente_obj = Cliente.objects.get(identificacion=formCliente['identificacion'].value())
            except Cliente.DoesNotExist:
                cliente_obj = formCliente.save()

            print(request.user.username)
            servicio = formServicio.save(commit=False)
            servicio.cliente = cliente_obj
            servicio.encargado = request.user
            servicio.ticket = genTicket()
            servicio.save()
            messages.success(request, mensaje_exito)
            # return HttpResponseRedirect(reverse_lazy(viewsRedirect))
            print("se envio")

        else: 
            print ('algun formulario esta invalido')
            print(formServicio.errors)
            print(formCliente.errors)

    else:
        formServicio = ServiciosForm(instance=servicio)
        formCliente = ClienteForm(instance=cliente)
        contexto = {'formServicio': formServicio, 'formCliente': formCliente}

    return render(request, 'registrar_servicio.html', contexto)


@login_required
@verificar_rol(roles_permitidos=['director', 'curador', 'investigador'])
def ListarServicio(request) : 
    servicios = Servicios.objects.all()
    print ('hi')
    print (servicios)
    contexto = {'servicios':servicios}
    return render(request,'listar_servicio.html', contexto )

def ConsultarServicio(request) : 
    return render(request, 'consultar_servicio.html' )


# class ServiciosList(ListView):
#     def dispatch(self, request, *args, **kwargs):
#         return super(ServiciosList, self).dispatch(request, *args, **kwargs)

#     model = Servicios
#     template_name = 'listar_servicio.html'

def genTicket(len=7):
    x = uuid4()
    return str(x)[:len]
