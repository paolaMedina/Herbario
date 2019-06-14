from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators  import  login_required
from django.shortcuts import render, HttpResponseRedirect
from servicios.models import Servicios
from servicios.forms import ServiciosForm
from cliente.models import Cliente
from cliente.forms import ClienteForm


# Create your views here.
@login_required
def RegistrarEspecimen(request, pk=None):

    if pk:
        print(pk)
        servicio = Servicios.objects.get(pk=pk)
        cliente = Cliente.objects.get(pk=servicio.cliente.pk)
        mensaje_exito = "Se edito exitosamente"
        # viewsRedirect='especimen:listar_especimen'

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
            servicio.save()
            messages.success(request, mensaje_exito)
            # return HttpResponseRedirect(reverse_lazy(viewsRedirect))
            print("se envio")

        else: 
            print ('algun formulario esta invalido')
            print(formServicio.errors)
            print(formCliente.errors)

    # else:
    formServicio = ServiciosForm(instance=servicio)
    formCliente = ClienteForm(instance=cliente)
    contexto = {'formServicio': formServicio, 'formCliente': formCliente}

    return render(request, 'registrar_servicio.html', contexto)
