from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail

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
       
			email_subject = 'Terminó servicio con Número de ticket'
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
def realizarPrestamo(request):
	prestamoForm = PrestamoForm()
	formCliente = ClienteForm()
	return render(request, 'prestamo.html', { 'prestamoForm':prestamoForm, 'formCliente':formCliente})

#@login_required
def listarSolicitudes(request):
	prestamo = Prestamo.objects.filter(estado='solicitud')
	contexto = {'prestamos':prestamo, 'nombre': 'Lista de solicitudes', 'prestamo': False}
	return render(request,'listar_prestamos.html', contexto )

#@login_required
def listarPrestamos(request):
	prestamo = Prestamo.objects.filter(estado='prestamo')
	contexto = {'prestamos':prestamo, 'nombre': 'Lista de solicitudes', 'prestamo': True}
	return render(request,'listar_prestamos.html', contexto )