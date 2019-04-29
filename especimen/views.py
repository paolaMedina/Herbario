#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
# from django.forms import ModelForm, inlineformset_factory
from django.forms import formset_factory
from .models import  Especimen
from .forms import EspecimenForm
from cientifico.models import Cientifico
from cientifico.forms import CientificoForm
from coleccion.models import Coleccion,Colectores
from coleccion.forms import ColeccionForm,ColectoresForm
from categoriaTaxonomica.models import CategoriaTaxonomica
from categoriaTaxonomica.forms import TaxonomiaForm
from ubicacion.models import Ubicacion
from ubicacion.forms import UbicacionForm
from django.contrib.auth.decorators  import  login_required
from rolepermissions.decorators import has_role_decorator
from django.shortcuts import get_object_or_404 
from django.shortcuts import redirect
from django.http import JsonResponse
from herbario1.utilities import *
import json
import types
from django.db import connection, transaction
import ast

@login_required
# # @has_role_decorator(['monitor', 'curador','investigador'])
@verificar_rol(roles_permitidos=['monitor', 'curador','investigador', 'director'])
def RegistrarEspecimen(request, pk=None):
    
    ColectoresFormSet = formset_factory(CientificoForm)
    dicColectoresSecu=[]
    #cargar datos en caso de ser edicion
    if pk:
        especimen = Especimen.objects.get(pk=pk)
        if (especimen.categoria != None):
            categoriaTaxo=CategoriaTaxonomica.objects.get(pk=especimen.categoria.pk)
        else:
            categoriaTaxo=CategoriaTaxonomica()
        if (especimen.coleccion != None):
            coleccionObje= Coleccion.objects.get(pk=especimen.coleccion.pk)
        else:
            coleccionObje=Coleccion()
        if (especimen.ubicacion != None):
            ubicacionObje=Ubicacion.objects.get(pk=especimen.ubicacion.pk)
        else:
            ubicacionObje=Ubicacion()
        if (especimen.coleccion != None and especimen.coleccion.colector_ppal != None):
            colectorppal=Cientifico.objects.get(pk=especimen.coleccion.colector_ppal.pk)
        else:
            colectorppal=Cientifico()
        if (especimen.determinador != None):
            determinadorObje=Cientifico.objects.get(pk=especimen.determinador.pk)
        else:
            determinadorObje= Cientifico()
        if (especimen.coleccion != None and coleccionObje.colectores_secu != None):
            cientificos= coleccionObje.colectores_secu.all()
            #rrecorre cientificos, que es la query con los colectores secundarios y crea un diccionario con estos para pasarlo por initial al formset
            for cientifico in cientificos:
                x={'nombre_completo':cientifico.nombre_completo,'nombre_abreviado':cientifico.nombre_abreviado}
                dicColectoresSecu.append(x)
        else:
            cientificos= Cientifico()
        

        mensaje_exito="Se edito exitosamente"
        viewsRedirect='especimen:listar_especimen'
        
        # print (dicColectoresSecu)
            
    else: 
        especimen = Especimen()
        categoriaTaxo=CategoriaTaxonomica()
        coleccionObje=Coleccion()
        ubicacionObje=Ubicacion()
        colectorppal=Cientifico()
        colectoresObje=Colectores()
        determinadorObje= Cientifico()
        cientificos=Cientifico()
        mensaje_exito='Se ha guardado exitosamente'
        viewsRedirect='especimen:crear_especimen'
    

    if request.method == 'POST':
        print ("solicitud post")
        
        #carga de formularios necesarios para cada modelo

        #cat_taxonomica
        formCateTaxonomica= TaxonomiaForm(request.POST,instance=categoriaTaxo)
        #coleccion
        formColector= CientificoForm (request.POST,prefix="colector", instance= colectorppal)
        formColeccion = ColeccionForm(request.POST,instance=coleccionObje)
        colectoresFormset = ColectoresFormSet(request.POST,initial=dicColectoresSecu)
        #ubicacion
        formUbicacion= UbicacionForm(request.POST,instance=ubicacionObje)
        #especimen
        formDeterminador= CientificoForm (request.POST,prefix="determinador",instance=determinadorObje)
        formEspecimen = EspecimenForm(request.POST, request.FILES,instance=especimen)
        
        colectorPpal=None
        determinador=None

        if formEspecimen.is_valid() and formCateTaxonomica.is_valid() and formColector.is_valid() and formColeccion.is_valid() and formUbicacion.is_valid(): 
            print("valido")
            if(formColector['nombre_completo'].value() != ""):
                try :
                    colectorPpal = Cientifico.objects.get(nombre_completo=formColector['nombre_completo'].value(),nombre_abreviado=formColector['nombre_abreviado'].value())
                except Cientifico.DoesNotExist:
                    colectorPpal = formColector.save()
            if(formDeterminador['nombre_completo'].value() != ""):
                try :
                    determinador = Cientifico.objects.get(nombre_completo=formDeterminador['nombre_completo'].value(),nombre_abreviado=formDeterminador['nombre_abreviado'].value())
                except Cientifico.DoesNotExist:
                    determinador = formDeterminador.save()

        #    validar que el formulario no venga completamente vacio
            if (formCateTaxonomica['familia'].value()=="" and formCateTaxonomica['genero'].value()=="" and formCateTaxonomica['epiteto_especifico'].value()=="" and formCateTaxonomica['fecha_det'].value()=="" and formCateTaxonomica['epiteto_infraespecifico'].value()=="" and formCateTaxonomica['categoria_infraespecifica'].value()=="" and formCateTaxonomica['autor1'].value()=="" and formCateTaxonomica['autor2'].value()=="" ):
                cateTaxonomica=None
            else:
                cateTaxonomica=formCateTaxonomica.save() 
            
            if (formUbicacion['pais'].value()=="" and formUbicacion['departamento'].value()=="" and formUbicacion['municipio'].value()=="" and formUbicacion['divisionPolitica'].value()=="" and formUbicacion['especificacionLocacion'].value()=="" and formUbicacion['latitud'].value()=="" and formUbicacion['longitud'].value()=="" and formUbicacion['alturaMinima'].value()=="" and formUbicacion['alturaMaxima'].value()=="" ):
                 ubicacion=None
            else:
                ubicacion=formUbicacion.save()
            
            if(formColeccion['fecha'].value() == "" and formColeccion['descripcion'].value() == "" and colectorPpal==None):
                fColeccion=None
            else:
                fColeccion = formColeccion.save(commit = False)
                fColeccion.colector_ppal=colectorPpal
                fColeccion.save()
            # print (colectoresFormset)   
            #guardar colectores secundarios
            
            if(colectoresFormset.has_changed()):
                i=0 # contador que maneja el orden en que se ingresen los colectores
                fColeccion = formColeccion.save()
                coleccionObje.colectores_secu.clear()#limpia las instancias de colectores
                for colector_form in colectoresFormset:
                    print (colector_form['nombre_completo'].value())
                    # se crea la colección en caso que que los campos fecha, descripción y col_principal no existieran, pero si secundarios
                        
                    try :
                        objeColector = Cientifico.objects.get(nombre_completo=colector_form['nombre_completo'].value(), nombre_abreviado=colector_form['nombre_abreviado'].value())
                    #print("existe")
                    except Cientifico.DoesNotExist:
                        objeColector=Cientifico(nombre_completo=colector_form['nombre_completo'].value(), nombre_abreviado=colector_form['nombre_abreviado'].value())
                        objeColector.save()
                        #print("se crea")
                
                    colectores= Colectores.objects.create(coleccion=fColeccion, colector=objeColector, orden=i)
                    i+=1
            especimen = formEspecimen.save(commit = False)    
            especimen.categoria=cateTaxonomica
            especimen.determinador=determinador  
            especimen.coleccion=fColeccion
            especimen.ubicacion=ubicacion
            especimen.usuario=request.user
            especimen.save()
            messages.success(request, mensaje_exito)
            return HttpResponseRedirect(reverse_lazy(viewsRedirect))
            print ("se envio")
        
        else: print ('algun formulario esta invalido')

    else:
        formCateTaxonomica= TaxonomiaForm(instance=categoriaTaxo)
        formColector= CientificoForm (prefix="colector", instance= colectorppal)
        formColeccion = ColeccionForm(instance=coleccionObje)
        colectoresFormset = ColectoresFormSet(initial=dicColectoresSecu)
        formEspecimen = EspecimenForm(instance=especimen)
        formDeterminador = CientificoForm (prefix="determinador",instance=determinadorObje)
        formUbicacion= UbicacionForm(instance=ubicacionObje)
    contexto={'formCateTaxonomica': formCateTaxonomica, 
              'formColector' :formColector,'formColeccion':formColeccion, 'colectoresFormset':colectoresFormset,
              'formDeterminador': formDeterminador, 'formEspecimen':formEspecimen,'cientificos':cientificos, 'formUbicacion':formUbicacion}
              
    
    return render(request,'form_wizard.html',contexto)
   
#funcion que permite autocompletar los nombres de cientifico 
def autocomplete(request):
    if request.is_ajax():
        queryset = Cientifico.objects.filter(nombre_completo__istartswith=request.GET.get('search', None))
       
        list = []        
        for i in queryset:
            list.append(i.nombre_completo)
        data = {
            'list': list,
        }
    return JsonResponse(data) 	


#funcion que lista los especimenes de la base de datos
@login_required
@verificar_rol(roles_permitidos=['director', 'curador','investigador'])
def ListarEspecimen(request): 
    especimen= Especimen.objects.filter(visible=True) #si no esta visible es por que se ha eliminado
    contexto = {'especimenes':especimen}
    return render(request,'especimen_listar.html', contexto )

#funcion que lista los especimenes creado por el monitor logueado de la base de datos
@login_required
@verificar_rol(roles_permitidos=['monitor'])
def ListarEspecimenesPersonales(request):
    print (request.user.id)
    especimen= Especimen.objects.filter(visible=True,usuario=request.user) #si no esta visible es por que se ha eliminado
    print (especimen)
    contexto = {'especimenes':especimen}
    return render(request,'especimen_listar.html', contexto )
    
#funcion que elimina un especimen dado    
@login_required
@verificar_rol(roles_permitidos=['monitor', 'curador','investigador'])
def EliminarEspecimen(request, pk):
    especimen= Especimen.objects.get(pk=pk)
    especimen.visible=False
    especimen.save()
    return HttpResponseRedirect(reverse_lazy('especimen:listar_especimen'))

def ChangeEspecimen(request, pk=None):
    #cargar datos en caso de ser edicion
    if pk:
        
        try:
            especimenObject = Especimen.objects.get( num_registro=pk)
            
            if (especimenObject.categoria != None):
               categoriaTaxoObje=CategoriaTaxonomica.objects.get(pk=especimenObject.categoria.pk)
            else:
                categoriaTaxoObje=CategoriaTaxonomica()

            if (especimenObject.determinador != None):
                determinadorObje=Cientifico.objects.get(pk=especimenObject.determinador.pk)
            else:
                determinadorObje= Cientifico()
            
            show=True
            print ('especime')
        except Especimen.DoesNotExist:
            messages.error(request, 'No existe un especimen con el número de registro ingresado')
            show=False
            print ("no especimen")
            return redirect('especimen:actualizar_especimen')
    else: 
        especimenObject = Especimen()
        categoriaTaxoObje=CategoriaTaxonomica()
        determinadorObje= Cientifico()
        print ("sin pk")
        show=False
        
    if request.method == 'POST':
        formCateTaxonomica= TaxonomiaForm(request.POST)
        formDeterminador= CientificoForm (request.POST,prefix="determinador")
        formEspecimen = EspecimenForm(instance=especimenObject)

        
        if formDeterminador.is_valid() and formCateTaxonomica.is_valid() : 
            change=categoriaTaxoObje.genero +','+ categoriaTaxoObje.familia +',' + determinadorObje.nombre_completo +','+ determinadorObje.nombre_abreviado +',' + categoriaTaxoObje.fecha_det +','+categoriaTaxoObje.epiteto_especifico + ',' + categoriaTaxoObje.autor1 +','+categoriaTaxoObje.epiteto_infraespecifico + ',' + categoriaTaxoObje.autor2
            print("valido")
            if(formDeterminador.has_changed()):
                print ("cambio determinador")
                try :
                    determinadorObje = Cientifico.objects.get(nombre_completo=formDeterminador['nombre_completo'].value(),nombre_abreviado=formDeterminador['nombre_abreviado'].value())
                except Cientifico.DoesNotExist:
                    determinadorObje = formDeterminador.save()
                
                especimenObject.determinador=determinadorObje
            if(formCateTaxonomica.has_changed()):
                print ("cambio determinador")
                categoriaTaxoObje.genero=formCateTaxonomica['genero'].value()
                categoriaTaxoObje.familia=formCateTaxonomica['familia'].value()
                categoriaTaxoObje.epiteto_especifico=formCateTaxonomica['epiteto_especifico'].value()
                categoriaTaxoObje.epiteto_infraespecifico=formCateTaxonomica['epiteto_infraespecifico'].value()
                categoriaTaxoObje.fecha_det=formCateTaxonomica['fecha_det'].value()
                categoriaTaxoObje.autor1=formCateTaxonomica['autor1'].value()
                categoriaTaxoObje.autor2=formCateTaxonomica['autor2'].value()
                categoriaTaxoObje.save()
                especimenObject.categoria=categoriaTaxoObje
            
            
            especimenObject.save()
            show=False 
            messages.success(request, 'Actualización de especimen '+ str(especimenObject.num_registro) )
        else:
            print ('formulario invalido')
            messages.error(request, 'Formulario invalido')
            show=True
        
    else:
        formCateTaxonomica= TaxonomiaForm(instance=categoriaTaxoObje)
        formEspecimen = EspecimenForm(instance=especimenObject)
        formDeterminador = CientificoForm (prefix="determinador",instance=determinadorObje)

    contexto={'formCateTaxonomica': formCateTaxonomica, 
              'formDeterminador': formDeterminador, 'formEspecimen':formEspecimen, 'show':show}
   
    return render(request,'updateEspecimen.html',contexto)
    
def searchEspecimen(request):           
    especimensObject=None
    seleccion = request.POST.get('option', None)
    filtro= request.POST.get('filtro', None).strip()
    if (filtro==""):
        return render(request, 'index-home.html')
    else:
        if(seleccion =='especie'):
            aux=filtro.split()
            if(len(aux)>1):
                gen=aux[0]
                epiteto=aux[1]
                especimensObject = Especimen.objects.filter(categoria__epiteto_especifico__icontains=epiteto).filter(categoria__genero__icontains=gen)
            else: especimensObject=[]
        elif(seleccion =='familia'):
            especimensObject = Especimen.objects.filter(categoria__familia__icontains=filtro)
        elif(seleccion =='genero'):
            especimensObject = Especimen.objects.filter(categoria__genero__icontains=filtro)
            
        contexto = {
            'especimenes': especimensObject
            }
        return render(request,'BusquedaBasica.html',contexto)
    
def autocompleteFilter(request):
    query=[]
    if request.is_ajax():
        type=request.GET.get('type', None)
        search = request.GET.get('search', '').capitalize()
        if(type =='especie'):
            aux=search.split()
            gen=aux[0]
            try:
                epiteto=aux[1]
                querySet = CategoriaTaxonomica.objects.filter(epiteto_especifico__istartswith=epiteto).filter(genero__istartswith=gen).values_list('genero','epiteto_especifico')
                query=[]
                for q in querySet:
                    concat= q[0]+" "+q[1]    
                    query.append(concat)
            except:
                querySet = CategoriaTaxonomica.objects.filter(genero__istartswith=gen).values_list('genero','epiteto_especifico')
                query=[]
                for q in querySet:
                    concat= q[0]+" "+q[1]    
                    query.append(concat) 
        elif(type =='familia'):
            query = CategoriaTaxonomica.objects.filter(familia__istartswith=search).values_list('familia',flat=True).distinct('familia')
        elif(type =='genero'):
            query = CategoriaTaxonomica.objects.filter(genero__istartswith=search).values_list('genero',flat=True).distinct('genero')
        
        list = []        
        for i in query:
            list.append(i )
            
        data ={'list': list,}
    else:
        data = 'fail'
        
    return JsonResponse(data)   
    
def busquedaAvanzada(request):
    especimenes=None
    genero= request.POST.get('genero')
    familia= request.POST.get('familia')
    tipo= request.POST.get('tipo')
    registro= request.POST.get('numeroRegistro')
    colector= request.POST.get('colectorprimario')
    pais= request.POST.get('pais')
    departamento=request.POST.get('departamento')
    municipio=request.POST.get('municipio')
    listQuery=[]
    if(genero != ""):
        dict ={} 
        dict['genero']=genero
        listQuery.append(dict)
    if (familia != ""):
        dict ={} 
        dict['familia']=familia
        listQuery.append(dict)
    if (tipo != "ninguno"):
        dict ={} 
        dict['tipo']=tipo
        listQuery.append(dict)
    if (registro != ""):
        dict ={} 
        dict['num_registro']=registro
        listQuery.append(dict)
    if (pais != ""):
        dict ={} 
        dict['pais']=pais
        listQuery.append(dict)
    if (departamento != ""):
        dict ={} 
        dict['departamento']=departamento
        listQuery.append(dict)
    if (municipio != ""):
        dict ={} 
        dict['municipio']=municipio
        listQuery.append(dict)
        
    if (colector != ""):
        dict ={} 
        dict['colector.nombre_completo']=colector
        listQuery.append(dict)
    if(len(listQuery)>0):
    # and colector == ""):
        condiciones=""
        i=0
        for value in listQuery:
            for key in value:
                if i>0:
                    condiciones +=" and "
                condiciones += "UPPER("+ key+ ") LIKE  UPPER('" + value[key] +"%')"
                i+=1
        select='SELECT especimen.id as pk,especimen.imagen, especimen.tipo,especimen.num_registro, taxonomia.familia, taxonomia.genero, taxonomia.epiteto_especifico, coleccion.id, colector.id as id_colector_ppal,colector.nombre_completo as colector_ppal, ubicacion.pais,ubicacion.departamento, ubicacion.municipio '

        join="""FROM especimen_especimen as especimen
                JOIN "categoriaTaxonomica_categoriataxonomica" as taxonomia
                ON especimen.categoria_id=taxonomia.id
                JOIN "coleccion_coleccion" as coleccion
                ON especimen.coleccion_id=coleccion.id
                JOIN "cientifico_cientifico" as colector
                ON coleccion.colector_ppal_id=colector.id
                JOIN "ubicacion_ubicacion" as ubicacion
                ON especimen.ubicacion_id=ubicacion.id"""
        query= select + join +" where "+condiciones
        especimenes=sql_select(query)

        if colector != "":
            distinct='select DISTINCT colector.id, colector.nombre_completo '
            queryColector=distinct + join + " where " + condiciones
            print (queryColector)
            colectores=sql_select(queryColector)
            context={ 'colectores':colectores, 'especimenes_dumps':json.dumps(especimenes)} 
            return render(request,'busquedaColectores.html',context) 
        else:
            return render(request,'busquedaColectores.html', {'especimenes':especimenes} ) 
    else:
        return render(request, 'index-home.html')

def busquedaColectores(request):
    especimenesIni= request.POST.get('especimenes') 
    lista = ast.literal_eval(especimenesIni)#convertir unicode a list
    colector= request.POST.get('colector')
    filtro=[]
    for item in lista:
        if (item['id_colector_ppal']==colector):
            filtro.append(item)
    # print (filtro)
    return JsonResponse({'data':filtro})   

def sql_select(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    list = []
    i = 0
    for row in results:
        dict = {} 
        field = 0
        while True:
            try:
                dict[cursor.description[field][0]] = str(results[i][field])
                field = field +1
            except IndexError as e:
                break
        i = i + 1
        list.append(dict) 
    return list  

def vistaEspecimen(request, pk):
    
    especimen = Especimen.objects.get(num_registro=pk)
    categoriaTaxo=CategoriaTaxonomica.objects.get(pk=especimen.categoria.pk)
    coleccionObje= Coleccion.objects.get(pk=especimen.coleccion.pk)
    ubicacionObje=Ubicacion.objects.get(pk=especimen.ubicacion.pk)
    colectorppal=Cientifico.objects.get(pk=especimen.coleccion.colector_ppal.pk)
    determinadorObje=Cientifico.objects.get(pk=especimen.determinador.pk)
    colecoresSecun= coleccionObje.colectores_secu.all()
    contexto={'especimen':especimen, 'taxonomia':categoriaTaxo,'coleccion':coleccionObje,'ubicacion':ubicacionObje,
                'colectorPpal':colectorppal,'determinador':determinadorObje,'colecoresSecun':colecoresSecun}

    return render(request,'detalleEspecimen.html',contexto)
