from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from .models import  Especimen
from cientifico.models import Cientifico
from cientifico.forms import CientificoForm
from coleccion.models import Coleccion,Colectores
from coleccion.forms import ColeccionForm,ColectoresForm
from categoriaTaxonomica.models import CategoriaTaxonomica
from categoriaTaxonomica.forms import TaxonomiaForm
from .forms import EspecimenForm
from django.forms import ModelForm, inlineformset_factory
from django.forms.formsets import formset_factory


import psycopg2, psycopg2.extras

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
            #return HttpResponseRedirect(reverse_lazy('especimen:crear_especimen'))
            
        
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
        

def ListarEspecimen(request):
    especimen= Especimen.objects.filter(visible=True)
    contexto = {'especimenes':especimen}
    return render(request,'especimen_listar.html', contexto )
        
def EliminarEspecimen(request, pk):
    especimen= Especimen.objects.get(pk=pk)
    especimen.visible_set=False
    #especimen.save()
    response = {}
    return HttpResponseRedirect(reverse_lazy('especimen:listar_especimen'))
    return JsonResponse(response) 