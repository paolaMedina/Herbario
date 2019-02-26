#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import CategoriaTaxonomica



class TaxonomiaForm(forms.ModelForm):


 class Meta:
        model = CategoriaTaxonomica
        fields = [
                'familia',
                'genero',
                'epiteto_especifico',
                'fecha_det',
                'categoria_infraespecifica',
                'epiteto_infraespecifico',
                'autor1',
                'autor2'
               
            ]
            
        labels = {
                'familia' : 'Familia',
                'genero' : 'Genero',
                'epiteto_especifico': 'Epiteto Especifico' ,
                'fecha_det' : 'Fecha Determinacion',
                'categoria_infraespecifica' : 'Categoria Infraespecifico',
                'epiteto_infraespecifico' : 'Epiteto Infraespecifico',
                'autor1' : 'Autor 1',
                'autor2' : 'Autor 2'
                
        }
        widgets = {
                'familia': forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12 ignored'}),
                'genero': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12 ignored'}),
                'epiteto_especifico': forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12 ignored'}),
                'fecha_det': forms.TextInput(attrs={'type':'text', 'id':'data_3', 'name':'datepicker', 'class':'form-control col-md-7 col-xs-12 ignored' }),
                'categoria_infraespecifica': forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12 ignored'}),
                'epiteto_infraespecifico' : forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12 ignored'}),
                'autor1' : forms.Textarea(attrs={'rows': '2', 'class':'form-control col-md-7 col-xs-12 ignored'}),
                'autor2' : forms.Textarea(attrs={ 'class':'form-control col-md-7 col-xs-12 ignored'}),
                
                

        }
        
