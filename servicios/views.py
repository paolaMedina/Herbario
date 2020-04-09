from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators  import  login_required
from django.shortcuts import render, HttpResponseRedirect
from django.core.mail import send_mail
from servicios.models import Servicios
from servicios.forms import ServiciosForm, ConsultarServicoForm
from cliente.models import Cliente
from cliente.forms import ClienteForm
from uuid import uuid4
from herbario1.utilities import *
from django.views.generic import ListView

# Create your views here.
@login_required
def RegistrarServicio(request, pk=None):

    if pk:
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

            servicio = formServicio.save(commit=False)
            servicio.cliente = cliente_obj
            if pk== None:
                servicio.encargado = request.user
                servicio.ticket = genTicket()
            servicio.save()
            messages.success(request, mensaje_exito)
            print("se envio")
            return HttpResponseRedirect(reverse_lazy('servicios:listar_servicio'))


        else: 
            print ('algun formulario esta invalido')
            print(formServicio.errors)
            print(formCliente.errors)
        contexto = {'formServicio': formServicio, 'formCliente': formCliente}
        

    else:
        formServicio = ServiciosForm(instance=servicio)
        formCliente = ClienteForm(instance=cliente)
        contexto = {'formServicio': formServicio, 'formCliente': formCliente}
        return render(request, 'registrar_servicio.html', contexto)


@login_required
@verificar_rol(roles_permitidos=['director', 'curador', 'investigador'])
def ListarServicio(request) : 
    servicios = Servicios.objects.all()
    contexto = {'servicios':servicios}
    return render(request,'listar_servicio.html', contexto )

@login_required
def ProcesarServicio (request, pk):
    try:
        servicio = Servicios.objects.get(pk=pk)
        servicio.estado = 'proceso'
        servicio.save()
        messages.success(request, 'Se ha actualizado el estado a proceso')
    except Servicios.DoesNotExist:
        messages.error(request, 'No existe el servicio en consulta')
        
    return HttpResponseRedirect(reverse_lazy('servicios:listar_servicio'))

@login_required
def CancelarServicio (request, pk):
    try:
        servicio = Servicios.objects.get(pk=pk)
        servicio.estado = 'cancelado'
        servicio.save()
        messages.success(request, 'Se ha actualizado el estado a cancelado')
    except Servicios.DoesNotExist:
        messages.error(request, 'No existe el servicio en consulta')
        
    return HttpResponseRedirect(reverse_lazy('servicios:listar_servicio'))
    

@login_required
def EntregarServicio (request, pk):
    try:
        servicio = Servicios.objects.get(pk=pk)
        servicio.estado = 'entregado'
        servicio.save()
        messages.success(request, 'Se ha actualizado el estado a entregado')
    except Servicios.DoesNotExist:
        messages.error(request, 'No existe el servicio en consulta')
        
    return HttpResponseRedirect(reverse_lazy('servicios:listar_servicio'))
    
@login_required
def VisualizarServicio (request, pk):
    try:
        servicio = Servicios.objects.get(pk=pk)
        cliente = servicio.cliente
    except Servicios.DoesNotExist:
        messages.error(request, 'No existe el servicio en consulta')
        return HttpResponseRedirect(reverse_lazy('servicios:listar_servicio'))

    formServicio = ServiciosForm(instance=servicio)
    formCliente = ClienteForm(instance=cliente)

    for field in formServicio.fields.items():
        field[1].widget.attrs['readonly'] = True

    for field in formCliente.fields.items():
        field[1].widget.attrs['readonly'] = True

    contexto = {'formServicio':formServicio, 'formCliente':formCliente}

    return render(request, 'registrar_servicio.html', contexto)

@login_required
def TerminarServicio (request, pk):
    try:
        servicio = Servicios.objects.get(pk=pk)
        servicio.estado = 'terminado'
        

        email = servicio.cliente.correo
        
        email_subject = 'Terminó servicio con Número de ticket ' + servicio.ticket

        email_body = "Buen día, \n el proceo  con Número de ticket: %s se ha marcado como terminado" % (servicio.ticket)

        send_mail(email_subject, email_body, 'angiepmc93@gmail.com', [email], fail_silently=False)

        servicio.save()
        messages.success(request, 'Se ha actualizado el estado a terminado')
    except Servicios.DoesNotExist:
        messages.error(request, 'No existe el servicio en consulta')
        
    return HttpResponseRedirect(reverse_lazy('servicios:listar_servicio'))
    
# class ServiciosList(ListView):
#     def dispatch(self, request, *args, **kwargs):
#         return super(ServiciosList, self).dispatch(request, *args, **kwargs)

#     model = Servicios
#     template_name = 'listar_servicio.html'

def consultarTicket(request):
    if request.method == 'GET':
        form = ConsultarServicoForm()
        contexto = {'form': form}
        return render(request, 'consultar_servicio.html', contexto)
    # e5ec846 - id servico
    elif request.method == 'POST':
        
        form = ConsultarServicoForm(request.POST, request.FILES)
        if form.is_valid():
            
            noTicket = form['ticket'].value() 
            try:
                servicio = Servicios.objects.get(ticket= noTicket)
                estado = servicio.estado

                if estado == 'solicitud':
                    mensaje = 'Estimado usuario le pedimos excusas en estos momentos no hemos empezado a trabajar en su solicitud, prometemos hacerlo pronto.'
                elif estado == 'proceso':
                    email = ocultar_email (servicio.cliente.correo)
                    mensaje = 'Estimado usuario en estos momentos estamos trabajando en su solicitud, una vez termine el proceso se le notificará al correo ' + email
                elif estado == 'terminado':
                    mensaje = 'Estimado usuario ya puede dirigirse a nuestras instalaciones, para hacerle entrega de su trabajo. Gracias por confiar en nosotros'
                elif estado == 'entregado':
                    mensaje = 'Estimado usuario, el trabajo solicitado ya ha sido entregado'
                else:
                    mensaje = 'Estimado usuario, el trabajo solicitado ha sido cancelado'

                form = ConsultarServicoForm(request.POST, request.FILES,instance=servicio)
                contexto = {'form': form, 'mensaje': mensaje}

                return render(request, 'consultar_servicio.html', contexto)
            except Servicios.DoesNotExist:
                messages.error(request, 'No existe el servicio en consulta')
                return HttpResponseRedirect(reverse_lazy('servicios:consultar_servicio'))
        else:
            messages.error(request, 'Por favor ingrese el número del ticket')
            return HttpResponseRedirect(reverse_lazy('servicios:consultar_servicio'))

def genTicket(len=7):
    x = uuid4()
    return str(x)[:len]
