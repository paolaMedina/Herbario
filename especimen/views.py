#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.forms import ModelForm, inlineformset_factory
from django.forms.formsets import formset_factory
from .models import  Especimen
from cientifico.models import Cientifico
from cientifico.forms import CientificoForm
from coleccion.models import Coleccion,Colectores
from coleccion.forms import ColeccionForm,ColectoresForm
from categoriaTaxonomica.models import CategoriaTaxonomica
from categoriaTaxonomica.forms import TaxonomiaForm
from .forms import EspecimenForm
from django.contrib.auth.decorators  import  login_required
from rolepermissions.decorators import has_role_decorator
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import JsonResponse
import json
import types
from django.db import connection, transaction

@login_required
@has_role_decorator(['monitor', 'curador','investigador'])
def RegistrarEspecimen(request, pk=None):
    
    ColectoresFormSet = formset_factory(CientificoForm)
    dicColectoresSecu=[]
    
    #cargar datos en caso de ser edicion
    if pk:
        especimen = Especimen.objects.get(pk=pk)
        categoriaTaxo=CategoriaTaxonomica.objects.get(pk=especimen.categoria.pk)
        coleccionObje= Coleccion.objects.get(pk=especimen.coleccion.pk)
        autor1Obje=Cientifico.objects.get(pk=especimen.categoria.autor1.pk)
        autor2Obje=Cientifico.objects.get(pk=especimen.categoria.autor2.pk)
        colectorppal=Cientifico.objects.get(pk=especimen.coleccion.colector_ppal.pk)
        determinadorObje=Cientifico.objects.get(pk=especimen.determinador.pk)
        cientificos= coleccionObje.colectores_secu.all()
        mensaje_exito="Se edito exitosamente"
        viewsRedirect='especimen:listar_especimen'
        
        #rrecorre cientificos, que es la query con los colectores secundarios y crea un diccionario con estos para pasarlo por initial al formset
        for cientifico in cientificos:
            x={'nombre_completo':cientifico.nombre_completo,'nombre_abreviado':cientifico.nombre_abreviado}
            dicColectoresSecu.append(x)
        
        #print dicColectoresSecu
            
    else: 
        especimen = Especimen()
        categoriaTaxo=CategoriaTaxonomica()
        coleccionObje=Coleccion()
        autor1Obje=Cientifico()
        autor2Obje=Cientifico()
        colectorppal=Cientifico()
        colectoresObje=Colectores()
        determinadorObje= Cientifico()
        cientificos=Cientifico()
        mensaje_exito='Se ha guardado exitosamente'
        viewsRedirect='especimen:crear_especimen'
        
    
    print especimen.imagen

    if request.method == 'POST':
        print ("solicitud post")
        
        #carga de formularios necesarios para cada modelo
        #cat_taxonomica
        formAutor1 = CientificoForm (request.POST,prefix="autor1",instance=autor1Obje)
        formAutor2 =  CientificoForm (request.POST,prefix="autor2",instance=autor2Obje)
        
        formCateTaxonomica= TaxonomiaForm(request.POST,instance=categoriaTaxo)
        
        #coleccion
        formColector= CientificoForm (request.POST,prefix="colector", instance= colectorppal)
        formColeccion = ColeccionForm(request.POST,instance=coleccionObje)
        colectoresFormset = ColectoresFormSet(request.POST,initial=dicColectoresSecu)
        #especimen
        formDeterminador= CientificoForm (request.POST,prefix="determinador",instance=determinadorObje)
        formEspecimen = EspecimenForm(request.POST, request.FILES,instance=especimen)
        
        if formAutor1.is_valid() and  formAutor2.is_valid() and formCateTaxonomica.is_valid() and formColector.is_valid() and formColeccion.is_valid() and formEspecimen.is_valid(): 
            print("valido")
            try :
                autor1 = Cientifico.objects.get(nombre_completo=formAutor1['nombre_completo'].value(),nombre_abreviado=formAutor1['nombre_abreviado'].value()) 
            except Cientifico.DoesNotExist:
                autor1 = formAutor1.save()
            try :
                autor2 = Cientifico.objects.get(nombre_completo=formAutor2['nombre_completo'].value(), nombre_abreviado=formAutor2['nombre_abreviado'].value())
            except Cientifico.DoesNotExist:
                autor2 = formAutor2.save()
            try :
                colectorPpal = Cientifico.objects.get(nombre_completo=formColector['nombre_completo'].value(),nombre_abreviado=formColector['nombre_abreviado'].value())
            except Cientifico.DoesNotExist:
                colectorPpal = formColector.save()
            try :
                determinador = Cientifico.objects.get(nombre_completo=formDeterminador['nombre_completo'].value(),nombre_abreviado=formDeterminador['nombre_abreviado'].value())
            except Cientifico.DoesNotExist:
                determinador = formDeterminador.save()
            
            cateTaxonomica=formCateTaxonomica.save(commit = False)    
            cateTaxonomica.autor1=autor1
            cateTaxonomica.autor2=autor2
            cateTaxonomica.save()
            
            fColeccion = formColeccion.save(commit = False)
            fColeccion.colector_ppal=colectorPpal
            fColeccion.save()
           
            #guardar colectores secundarios
            
            i=0# contador que maneja el orden en que se ingresen los colectores
            
            coleccionObje.colectores_secu.clear()#limpia las instancias de colectores
            #print (colectoresFormset.as_table()) 

            for colector_form in colectoresFormset:
                if not(colector_form['nombre_completo'].value()==""):
                    
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
            especimen.save()
            print ("se envio")
            
            messages.success(request, mensaje_exito)
            return HttpResponseRedirect(reverse_lazy(viewsRedirect))
            
        
    else:
        print ("solicitud get")
        formAutor1 = CientificoForm (prefix="autor1", instance=autor1Obje)
        formAutor2 =  CientificoForm (prefix="autor2",instance=autor2Obje)
        formCateTaxonomica= TaxonomiaForm(instance=categoriaTaxo)
        formColector= CientificoForm (prefix="colector", instance= colectorppal)
        formColeccion = ColeccionForm(instance=coleccionObje)
        colectoresFormset = ColectoresFormSet(initial=dicColectoresSecu)
        formEspecimen = EspecimenForm(instance=especimen)
        formDeterminador = CientificoForm (prefix="determinador",instance=determinadorObje)
        
    contexto={'formAutor1':formAutor1, 'formAutor2': formAutor2,'formCateTaxonomica': formCateTaxonomica, 
              'formColector' :formColector,'formColeccion':formColeccion, 'colectoresFormset':colectoresFormset,
              'formDeterminador': formDeterminador, 'formEspecimen':formEspecimen,'cientificos':cientificos}
              
    
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
def ListarEspecimen(request): 
    especimen= Especimen.objects.filter(visible=True)
    contexto = {'especimenes':especimen}
    return render(request,'especimen_listar.html', contexto )
    
    

#funcion que elimina un especimen dado    
@login_required   
def EliminarEspecimen(request, pk):
    especimen= Especimen.objects.get(pk=pk)
    especimen.visible_set=False
    #especimen.save()
    response = {}
    return HttpResponseRedirect(reverse_lazy('especimen:listar_especimen'))

def ChangeEspecimen(request, pk=None):
      #cargar datos en caso de ser edicion
    print pk
    if pk:
        
        try:
            especimenObject = Especimen.objects.get( num_registro=pk)
            categoriaTaxoObje=CategoriaTaxonomica.objects.get(pk=especimenObject.categoria.pk)
            autor1Obje=Cientifico.objects.get(pk=especimenObject.categoria.autor1.pk)
            autor2Obje=Cientifico.objects.get(pk=especimenObject.categoria.autor2.pk)
            determinadorObje=Cientifico.objects.get(pk=especimenObject.determinador.pk)
            show=True
            print 'especime'
        except Especimen.DoesNotExist:
            messages.error(request, 'No existe un especimen con el número de registro ingresado')
            show=False
            print"no especimen"
            return redirect('especimen:obtener_especimen')
        
       
    else: 
        especimenObject = Especimen()
        categoriaTaxoObje=CategoriaTaxonomica()
        autor1Obje=Cientifico()
        autor2Obje=Cientifico()
        determinadorObje= Cientifico()
        print"sin pk"
        show=False
        
        
    if request.method == 'POST':
        
        formAutor1 = CientificoForm (request.POST,prefix="autor1",instance=autor1Obje)
        formAutor2 =  CientificoForm (request.POST,prefix="autor2",instance=autor2Obje)
        
        formCateTaxonomica= TaxonomiaForm(request.POST,instance=categoriaTaxoObje)
        
        #especimen
        formDeterminador= CientificoForm (request.POST,prefix="determinador",instance=determinadorObje)
        formEspecimen = EspecimenForm(instance=especimenObject)
        
        #and formCateTaxonomica.is_valid() ---falta corregir esto
        if formAutor1.is_valid() and  formAutor2.is_valid() : 
            print("valido")
            
            try :
                autor1Obje = Cientifico.objects.get(nombre_completo=formAutor1['nombre_completo'].value(),nombre_abreviado=formAutor1['nombre_abreviado'].value()) 
            except Cientifico.DoesNotExist:
                autor1Obje = formAutor1.save()
            try :
                autor2Obje = Cientifico.objects.get(nombre_completo=formAutor2['nombre_completo'].value(), nombre_abreviado=formAutor2['nombre_abreviado'].value())
            except Cientifico.DoesNotExist:
                autor2Obje = formAutor2.save()
            try :
                determinadorObje = Cientifico.objects.get(nombre_completo=formDeterminador['nombre_completo'].value(),nombre_abreviado=formDeterminador['nombre_abreviado'].value())
            except Cientifico.DoesNotExist:
                determinadorObje = formDeterminador.save()
            
            
            categoriaTaxoObje.genero=formCateTaxonomica['genero'].value()
            categoriaTaxoObje.familia=formCateTaxonomica['familia'].value()
            categoriaTaxoObje.epiteto_especifico=formCateTaxonomica['epiteto_especifico'].value()
            categoriaTaxoObje.epiteto_infraespecifico=formCateTaxonomica['epiteto_infraespecifico'].value()
            categoriaTaxoObje.fecha_det=formCateTaxonomica['fecha_det'].value()
            categoriaTaxoObje.autor1=autor1Obje
            categoriaTaxoObje.autor2=autor2Obje
            categoriaTaxoObje.save()
            
            especimenObject.determinador=determinadorObje
            especimenObject.save()
            show=False 
            
        else:
            print ' formulario invalido'
            show=True
        
    else:
        formCateTaxonomica= TaxonomiaForm(instance=categoriaTaxoObje)
        formEspecimen = EspecimenForm(instance=especimenObject)
        formAutor1 = CientificoForm (prefix="autor1", instance=autor1Obje)
        formAutor2 =  CientificoForm (prefix="autor2",instance=autor2Obje)
        formDeterminador = CientificoForm (prefix="determinador",instance=determinadorObje)
        print show
        
        
        
    contexto={'formAutor1':formAutor1, 'formAutor2': formAutor2,'formCateTaxonomica': formCateTaxonomica, 
              'formDeterminador': formDeterminador, 'formEspecimen':formEspecimen, 'show':show}
   
    return render(request,'updateEspecimen.html',contexto)
    

def searchEspecimen(request):
    especimensObject=None
    print"aqui"
    print request.POST
    print request.POST.get('option', None)
    seleccion = request.POST.get('option', None)
    filtro= request.POST.get('filtro', None)
    
    if(seleccion =='especie'):
        especimensObject = Especimen.objects.filter(categoria__epiteto_especifico__icontains=filtro)
    elif(seleccion =='familia'):
        especimensObject = Especimen.objects.filter(categoria__familia__icontains=filtro)
    elif(seleccion =='genero'):
        especimensObject = Especimen.objects.filter(categoria__genero__icontains=filtro)
        
    contexto = {
        'especimenes': especimensObject
        }
    print contexto
    return render(request,'testing.html',contexto)
    

def autocompleteFilter(request):
    query=[]
    if request.is_ajax():
        type=request.GET.get('type', None)
        search = request.GET.get('search', '').capitalize()
        if(type =='especie'):
            query = CategoriaTaxonomica.objects.filter(epiteto_especifico__istartswith=search).values_list('epiteto_especifico',flat=True).distinct('epiteto_especifico')
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
    print request.POST
    genero= request.POST.get('genero')
    familia= request.POST.get('familia')
    tipo= request.POST.get('tipo')
    registro= request.POST.get('numeroRegistro')
    registro= request.POST.get('colectorprimario')
    listQuery=[]
    if(genero != ""):
        dict ={} 
        dict['genero']=genero
        listQuery.append(dict)
    if (familia != ""):
        dict ={} 
        dict['familia']=familia
        listQuery.append(dict)
        
    print listQuery
    condiciones=""
    i=0
    for value in listQuery:
        for key in value:
            if i>0:
                condiciones +=" and "
            condiciones += "UPPER("+ key+ ") LIKE  UPPER('" + value[key] +"%')"
            i+=1
        
    print condiciones
    
    query="""SELECT especimen.num_registro, taxonomia.familia, taxonomia.genero, taxonomia.epiteto_especifico, coleccion.id, colector.nombre_completo
                    FROM especimen_especimen as especimen
                    JOIN "categoriaTaxonomica_categoriataxonomica" as taxonomia
                    ON especimen.categoria_id=taxonomia.id
                    JOIN "coleccion_coleccion" as coleccion
                    ON especimen.coleccion_id=coleccion.id
                    JOIN "cientifico_cientifico" as colector
                    ON coleccion.colector_ppal_id=colector.id
                   """
    if condiciones != "":
        query=query+"where "+condiciones
        a=sql_select(query)
        print a
    return HttpResponseRedirect(reverse_lazy('inicio'))





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