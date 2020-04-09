from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators  import  login_required
from datetime import datetime

from .models import Prestamo
from .forms import SolicitudForm, PrestamoForm
from cliente.models import Cliente
from cliente.forms import ClienteForm
from usuario.models import Usuario



def solicitudPrestamo(request) :
    if request.method == 'GET':
        solicitudForm = SolicitudForm()
        formCliente = ClienteForm()
        return render(request, 'solicitud.html', { 'solicitudForm':solicitudForm, 'formCliente':formCliente})
    elif request.method == 'POST':
        solicitudForm = SolicitudForm(request.POST, request.FILES)
        formCliente = ClienteForm(request.POST, request.FILES)

        if solicitudForm.is_valid() and formCliente.is_valid():
            try:
                cliente_obj = Cliente.objects.get(identificacion=formCliente['identificacion'].value())
            except Cliente.DoesNotExist:
                cliente_obj = formCliente.save()

            prestamo = solicitudForm.save(commit=False)
            prestamo.cliente = cliente_obj            
            
            emails = []
            curadores = Usuario.objects.filter(rol='curador')
            for curador in curadores:
                emails.append(curador.email)

            directores = Usuario.objects.filter(rol='director')
            for director in directores:
                emails.append(director.email)

            emails.append(cliente_obj.correo)
       
            email_subject = 'Solicitud prestamo'
            email_body = "Buen día, \n Se ha realizado la solicitud de prestamo exitosamente"
            send_mail(email_subject, email_body, 'angiepmc93@gmail.com', emails, fail_silently=False)

            prestamo.save()
            messages.success(request, "Se ha realizado la solicitud de prestamo exitosamente")
            return HttpResponseRedirect(reverse_lazy('prestamo:solicitar_prestamo'))
        else:
            prestamo = Prestamo()
            cliente = Cliente()
            solicitudForm = SolicitudForm(request.POST, request.FILES, instance=prestamo)
            formCliente = ClienteForm(request.POST, request.FILES, instance=cliente)
            messages.error(request, 'Por favor verifique los campos del formulario')
            return render(request, 'solicitud.html', { 'solicitudForm':solicitudForm, 'formCliente':formCliente})


#@login_required
def cancelarSolicitud (request, pk):
    try:
        prestamo = Prestamo.objects.get(pk = pk)
        prestamo.estado = 'cancelado'

        email = prestamo.cliente.correo

        email_subject = 'Cancelación solicitud de prestamo '

        email_body = "Buen día, \n" 
        email_body += "Su solicitud %s ha sido cancelada" % (prestamo.solicitud)

        send_mail(email_subject, email_body, 'angiepmc93@gmail.com', [email], fail_silently=False)

        prestamo.save()
        messages.success(request, 'La solicitud se ha cancelado exitosamente')
    except Prestamo.DoesNotExist:
        messages.error(request, 'No existe la solicitud en consulta')

    return HttpResponseRedirect(reverse_lazy('prestamo:listar_solicitud'))

@login_required
def realizarPrestamo(request, pk):
    if request.method == 'GET':
        prestamo = Prestamo()
        cliente = Cliente()
        try:
            prestamo = Prestamo.objects.get(pk = pk)
            cliente = prestamo.cliente
            prestamoForm = PrestamoForm(instance=prestamo)
            formCliente = ClienteForm(instance=cliente)
            
            return render(request, 'prestamo.html', { 'prestamoForm':prestamoForm, 'formCliente':formCliente})
        
        except Prestamo.DoesNotExist:
            messages.error(request, 'No existe la solicitud en consulta')
            return HttpResponseRedirect(reverse_lazy('prestamo:listar_solicitud'))
        
    elif request.method == 'POST':
        prestamoForm = PrestamoForm(request.POST, request.FILES)
        formCliente = ClienteForm(request.POST, request.FILES)
        
        try:
            prestamo = Prestamo.objects.get(pk = pk)
            cliente = prestamo.cliente
        except Prestamo.DoesNotExist:
            messages.error(request, 'No existe la solicitud en consulta')
            return HttpResponseRedirect(reverse_lazy('prestamo:listar_solicitud'))

        if prestamoForm.is_valid() and formCliente.is_valid():
            prestamo.solicitud = prestamoForm['solicitud'].value()
            prestamo.num_registro = prestamoForm['num_registro'].value()
            prestamo.fecha_entrega = datetime.now()
            prestamo.fecha_devolucion = prestamoForm['fecha_devolucion'].value()
            prestamo.observaciones_entrega = prestamoForm['observaciones_entrega'].value()
            prestamo.encargado = request.user

            cliente.nombre_completo = formCliente['nombre_completo'].value()
            cliente.tipo_identificacion = formCliente['tipo_identificacion'].value()
            cliente.identificacion = formCliente['identificacion'].value()
            cliente.correo = formCliente['correo'].value()
            cliente.num_contacto = formCliente['num_contacto'].value()
            
            prestamo.cliente = cliente
            prestamo.estado = 'prestamo'
            cliente.save()
            prestamo.save()

            messages.success(request, 'Se ha realizado el prestamo con éxito')
            return HttpResponseRedirect(reverse_lazy('prestamo:listar_solicitud'))

        else:
            messages.error(request, 'Por favor verifique los datos del formulario')
            prestamoForm = PrestamoForm(request.POST, request.FILES, instance=prestamo)
            formCliente = ClienteForm(request.POST, request.FILES, instance=cliente)
            return render(request, 'prestamo.html', { 'prestamoForm':prestamoForm, 'formCliente':formCliente})

@login_required
def renovar_prestamo (request, pk):
    try:
        prestamo = Prestamo.objects.get(pk = pk)
        prestamo.fecha_entrega = prestamo.fecha_entrega + datetime.timedelta(days=15)
        
        email_subject = 'Renovación de prestamo '

        email_body = "Buen día, \n" 
        email_body += "Su prestamo %s ha sido renovado hasta el día " % (prestamo.solicitud, prestamo.fecha_entrega)

        send_mail(email_subject, email_body, 'angiepmc93@gmail.com', [email], fail_silently=False)

        prestamo.save()
        messages.success("Se ha renovado el prestamo exitosamente")
    except Prestamo.DoesNotExist:
        messages.error("El prestamo en consulta no existe")
    
    return HttpResponseRedirect(reverse_lazy('prestamo:listar_prestamo'))

@login_required
def entregar_prestamo (request, pk):
    try:
        prestamo = Prestamo.objects.get(pk = pk)
        prestamo.estado = 'entregado'
        prestamo.save()
        messages.success("El prestamo se ha regresado exitosamente")
    except Prestamo.DoesNotExist:
        messages.error("El prestamo en consulta no existe")
    
    return HttpResponseRedirect(reverse_lazy('prestamo:listar_prestamo'))

@login_required
def visualizar_prestamo (request, pk):
    try:
        prestamo = Prestamo.objects.get(pk=pk)
        cliente = prestamo.cliente
    except Prestamo.DoesNotExist:
        messages.error("El prestamo en consulta no existe")
        return HttpResponseRedirect(reverse_lazy('prestamo:listar_prestamo'))

    prestamoForm = PrestamoForm(instance=prestamo)
    formCliente = ClienteForm(instance=cliente)

    for field in prestamoForm.fields.items():
        field[1].widget.attrs['readonly'] = True

    for field in formCliente.fields.items():
        field[1].widget.attrs['readonly'] = True

    contexto = {'prestamoForm':prestamoForm, 'formCliente':formCliente}

    return render(request, 'prestamo.html', contexto)

@login_required
def listarSolicitudes(request):
    prestamo = Prestamo.objects.filter(estado='solicitud')
    contexto = {'prestamos':prestamo, 'nombre': 'Lista de solicitudes', 'listaprestamo': False}
    return render(request,'listar_prestamos.html', contexto )

@login_required
def listarPrestamos(request):
    prestamo = Prestamo.objects.filter(estado='prestamo')
    contexto = {'prestamos':prestamo, 'nombre': 'Lista de solicitudes', 'listaprestamo': True}
    return render(request,'listar_prestamos.html', contexto )