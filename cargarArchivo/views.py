# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import FormUpload
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
import os
from herbario1.utilities import *
import csv
import io
from cientifico.models import Cientifico
from coleccion.models import Coleccion,Colectores
from categoriaTaxonomica.models import CategoriaTaxonomica
from especimen.models import Especimen
from ubicacion.models import Ubicacion


class UploadFileView(FormView):
    '''
    Esta vista sube un archivo al servidor
    '''
    template_name = "upload.html"
    form_class = FormUpload
    success_url = reverse_lazy("archivo:upload")
    
    
    """@verificar_rol(roles_permitidos=["administrador","ingeniero"])
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFileView, self).dispatch(request, *args, **kwargs)"""
    
    def get(self, request, *args, **kwargs):
        data = {'form': self.form_class}
        return render(request, self.template_name, data)
 
    def post(self, request, *args, **kwargs):
        form = FormUpload(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            print file
            handle_uploaded_file(file)
        return self.form_valid(form, **kwargs)
        
   
            
#Para guardar la iniformacion en los archivos ya existentes o crear uno nuevo y guardar             
def handle_uploaded_file(csv_file):
    print csv_file
    decoded_file = csv_file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    
    reader=csv.DictReader(io_string, delimiter=str(u','))#CAMBIAR
    reader.next()
    #print reader.next()
    
    for line in  reader:
        
        
        #limpiar espacios en blanco y solo obtener los valores antes del punto para fecha
        fecha_determinacion= formatDate(line['DETMM'].strip(' '),line['DETDD'].strip(' '),line['DETYY'].strip(' '))
        
        
        try :
            colectorPpal = Cientifico.objects.get(nombre_completo=line['COLLECTOR'])
        except Cientifico.DoesNotExist:
            colectorPpal =Cientifico(nombre_completo=line['COLLECTOR'])
            colectorPpal.save()
            
        print line['DETBY']
        try :
            objdeterminador = Cientifico.objects.get(nombre_completo=line['DETBY'], nombre_abreviado="")
        except Cientifico.DoesNotExist:
            objdeterminador =Cientifico(nombre_completo=line['DETBY'])
            objdeterminador.save()    
            
        
        cateTaxonomica=CategoriaTaxonomica(familia=line['FAMILY'],genero=line['GENUS'],epiteto_especifico=line['SP1'],
                                           fecha_det=fecha_determinacion,categoria_infraespecifica=line['RANK1'],
                                           epiteto_infraespecifico=line['SP2'],autor1=line['AUTHOR1'],autor2=line['AUTHOR2']) 
        cateTaxonomica.save()
        
        fecha_coleccion= formatDate(line['COLLMM'].strip(' '),line['COLLDD'].strip(' '),line['COLLYY'].strip(' '))
        
        objcoleccion= Coleccion(colector_ppal=colectorPpal,fecha=fecha_coleccion,descripcion=line['PLANTDESC'])
        objcoleccion.save()
        
        colectoresSec=line['ADDCOLL'].split('.,')#arreglo de colectores secundarios
        i=0# contador que maneja el orden en que se ingresen los colectores
        for colector in colectoresSec:
            try :
               objeColector = Cientifico.objects.get(nombre_completo=colector)
            except Cientifico.DoesNotExist:
                objeColector=Cientifico(nombre_completo=colector)
                objeColector.save()
            colectores= Colectores.objects.create(coleccion=objcoleccion, colector=objeColector, orden=i)
            i+=1
        
        if (line['LONG'].strip()==""):
            long=None
        else:
            try:
                long=float(line['LONG'].strip())
            except:
                long=None
                

        if (line['LAT'].strip()==""):
            lat=None
        else:
            try:
                lat=float(line['LAT'].strip())
            except:
                lat=None
        
        print long
        print lat
        objUbicacion=Ubicacion(pais=line['COUNTRY'],departamento=line['MAJORAREA'],municipio=line['MINORAREA'],divisionPolitica=line['GAZETTEER'],latitud= lat ,longitud= long,especificacionLocacion=line['LOCNOTES'], cultivada=True)
        objUbicacion.save()

        especimen=Especimen(num_registro=line['ACCESSION'],categoria=cateTaxonomica,coleccion=objcoleccion,
                            determinador=objdeterminador,lugar_duplicado= line['DUPS'] ,peligro='FP', tipo='holo', ubicacion=objUbicacion,visible=True)
        especimen.save()
    
def formatDate(month,day,year):
    return month.split(".")[0]+"/"+day.split(".")[0]+"/"+year.split(".")[0]
        