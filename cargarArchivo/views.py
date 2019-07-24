# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import FormUpload
from django.urls import reverse_lazy
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
    
    
    @verificar_rol(roles_permitidos=["director","curador", "investigador"])
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFileView, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        data = {'form': self.form_class}
        return render(request, self.template_name, data)
 
    def post(self, request, *args, **kwargs):
        form = FormUpload(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            result=handle_uploaded_file(file)
            if result==True:
                messages.success(self.request, 'El archivo cargo con exito')
            else:
                messages.error(self.request,'No se pudo cargar archivo, por favor revisar la codificación del archivo')

        return self.form_valid(form, **kwargs)
        
   
            
#Para guardar la iniformacion en los archivos ya existentes o crear uno nuevo y guardar  

         
def handle_uploaded_file(csv_file):
    try:
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader=csv.DictReader(io_string, delimiter=str(u','))#CAMBIAR
        for line in  reader:
            # print (line)
            # print ("--------------------------------------------------------------------")
            try:
                especimen=Especimen.objects.get(num_registro=line['ACCESSION'])
            except Especimen.DoesNotExist:
                especimen=Especimen()

            #limpiar espacios en blanco y solo obtener los valores antes del punto para fecha
            fecha_determinacion= formatDate(line['DETMM'].strip(' '),line['DETDD'].strip(' '),line['DETYY'].strip(' '))
            #print (fecha_determinacion)
            try :
                colectorPpal = Cientifico.objects.get(nombre_completo=line['COLLECTOR'])
            except Cientifico.DoesNotExist:
                if(line['COLLECTOR'] != ""):
                    colectorPpal =Cientifico(nombre_completo=line['COLLECTOR'])
                    colectorPpal.save()
                else:
                    colectorPpal=None
            try :
                objdeterminador = Cientifico.objects.get(nombre_completo=line['DETBY'])
            except Cientifico.DoesNotExist:
                if(line['DETBY'] != ""):
                    objdeterminador =Cientifico(nombre_completo=line['DETBY'])
                    objdeterminador.save()    
                else:
                    objdeterminador= None
            
            if(especimen.categoria ):
                especimen.categoria.delete()

            cateTaxonomica=CategoriaTaxonomica(familia=line['FAMILY'],genero=line['GENUS'],epiteto_especifico=line['SP1'],
                                            fecha_det=fecha_determinacion,categoria_infraespecifica=line['RANK1'],
                                            epiteto_infraespecifico=line['SP2'],autor1=line['AUTHOR1'],autor2=line['AUTHOR2']) 
            cateTaxonomica.save()
            
            fecha_coleccion= formatDate(line['COLLMM'].strip(' '),line['COLLDD'].strip(' '),line['COLLYY'].strip(' '))

            numeroColeccion = line['PREFIX'].strip(' ') + line['NUMBER'].strip(' ') + line['SUFFIX'].strip(' ')
            
            if(especimen.coleccion):
                especimen.coleccion.delete()

            objcoleccion= Coleccion(colector_ppal=colectorPpal,fecha=fecha_coleccion,descripcion=line['PLANTDESC'], numero=numeroColeccion)
            objcoleccion.save()
            
            colectoresSec=line['ADDCOLL'].split('.,')#arreglo de colectores secundarios
            i=0# contador que maneja el orden en que se ingresen los colectores
            for colector in colectoresSec:
                try :
                    objeColector = Cientifico.objects.get(nombre_completo=colector)
                except Cientifico.DoesNotExist:
                    if(colector != ""):
                        objeColector=Cientifico(nombre_completo=colector)
                        objeColector.save()
                        colectores= Colectores.objects.create(coleccion=objcoleccion, colector=objeColector, orden=i)
                        i+=1
            
            if (line['LONG'].strip()==""):
                long=None
            else:
                try:
                    number =float(line['LONG'].strip())
                    if(number/1 !=0):
                        long=number
                    else:
                        long=None
                except:
                    long=None
                    

            if (line['LAT'].strip()==""):
                lat=None
            else:
                try:
                    number=float(line['LAT'].strip())
                    if(number/1 != 0):
                        lat=number
                    else:
                        lat=None
                except:
                    lat=None

            if (line['NS'].strip()==""):
                posicionLat='ninguno'
            else:
                posicionLat=line['NS'].strip()
            
            if (line['EW'].strip()==""):
                posicionLong='ninguno'
            else:
                posicionLong=line['EW'].strip()
            
            if (line['ALT'].strip()==""):
                alturaMinima=None
            else:
                try:
                    alturaMinima=float(line['ALT'].strip())
                except:
                    alturaMinima=None
            
            if (line['ALTMAX'].strip()==""):
                alturaMaxima=None
            else:
                try:
                    alturaMaxima=float(line['ALTMAX'].strip())
                except:
                    alturaMaxima=None
            
            if (line['ALTUNIT'].strip()==""):
                altUni=None
            else:
                altUni=line['ALTUNIT'].strip()
                
            if(especimen.ubicacion):
                especimen.ubicacion.delete()

            objUbicacion=Ubicacion(pais=line['COUNTRY'],departamento=line['MAJORAREA'],municipio=line['MINORAREA'],divisionPolitica=line['GAZETTEER'],latitud= lat ,longitud= long,especificacionLocacion=line['LOCNOTES'],posicionLat=posicionLat,posicionLong=posicionLong, alturaMinima=alturaMinima,alturaMaxima=alturaMaxima,altUni=altUni, 
            cultivada=True)
            objUbicacion.save()
            #print (objUbicacion)
            especimen.num_registro=line['ACCESSION']
            especimen.lugar_duplicado= line['DUPS']
            especimen.tipo='NoTipo'
            especimen.categoria=cateTaxonomica
            especimen.coleccion=objcoleccion
            especimen.determinador=objdeterminador
            especimen.ubicacion=objUbicacion
            especimen.visible=True
            especimen.usuario=None
            
            #especimen=Especimen(num_registro=line['ACCESSION'],categoria=cateTaxonomica,coleccion=objcoleccion,determinador=objdeterminador,lugar_duplicado= line['DUPS'] ,peligro='LC', tipo='NoTipo', ubicacion=objUbicacion,visible=True, usuario=None)
            #print (especimen)
            
            especimen.save()

        
        return True
    except Exception as e:
        print(e)
        return False
        

    
def formatDate(month,day,year):
    return month.split(".")[0]+"/"+day.split(".")[0]+"/"+year.split(".")[0]
        