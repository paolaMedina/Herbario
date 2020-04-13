from django.shortcuts import render

# Create your views here.

def SolcitudCubiculo(request):
    return render(request,'solicitud_cubiculo.html' )

def ListarSolicitud(request):
    return render(request,'listado_solicitudes.html' )

def listarCubiculo(request):
    return render(request,'listado_cubiculo.html' )
