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



def RegistrarEspecimen(request):
    
    ColectoresFormSet = formset_factory(ColectoresForm)

    if request.method == 'POST':
        print ("solicitud post")
        
        #carga de formularios necesarios para cada modelo
        #cat_taxonomica
        formAutor1 = CientificoForm (request.POST,prefix="autor1")
        formAutor2 =  CientificoForm (request.POST,prefix="autor2")
        formCateTaxonomica= TaxonomiaForm(request.POST)
        
        #coleccion
        formColector= CientificoForm (request.POST,prefix="colector")
        formColeccion = ColeccionForm(request.POST)
        colectoresFormset = ColectoresFormSet(request.POST)
        #especimen
        formDeterminador= CientificoForm (request.POST,prefix="determinador")
        formEspecimen = EspecimenForm(request.POST, request.FILES)
        
        

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
           
            
            #guardar formset
            
            i=0
            #print (colectoresFormset.as_table())

            for colector_form in colectoresFormset:
                if not(colector_form['nombre'].value()==""):
                    try :
                       objeColector = Cientifico.objects.get(nombre_completo=colector_form['nombre'].value(), nombre_abreviado=colector_form['abreviatura'].value())
                       print("existe")
                       
                    except Cientifico.DoesNotExist:
                        objeColector=Cientifico(nombre_completo=colector_form['nombre'].value(), nombre_abreviado=colector_form['abreviatura'].value())
                        print("se crea")
                        
                     
                    colectores= Colectores(coleccion=fColeccion, colector=objeColector, orden=i)
                    colectores.save()
                    i+=1 
            
            
            
            especimen = formEspecimen.save(commit = False)
            especimen.categoria=cateTaxonomica
            especimen.determinador=determinador
            especimen.coleccion=fColeccion
            especimen.save()
            print ("se envio")
            
            messages.success(request, 'Se ha guardado exitosamente')
            #return HttpResponseRedirect(reverse_lazy('especimen:crear_especimen'))
            
        
    else:
        print ("solicitud get")
        formAutor1 = CientificoForm (prefix="autor1")
        formAutor2 =  CientificoForm (prefix="autor2")
        formCateTaxonomica= TaxonomiaForm()
        formColector= CientificoForm (prefix="colector")
        formColeccion = ColeccionForm()
        colectoresFormset = ColectoresFormSet()
        formEspecimen = EspecimenForm()
        formDeterminador = CientificoForm (prefix="determinador")
       
   
        
        
    return render(request,'form_wizard.html',{'formAutor1':formAutor1, 'formAutor2': formAutor2,'formCateTaxonomica': formCateTaxonomica, 
                                                    'formColector' :formColector,'formColeccion':formColeccion, 'colectoresFormset':colectoresFormset,
                                                    'formDeterminador': formDeterminador, 'formEspecimen':formEspecimen})
   
    
    
    
    
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
        
