#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Ubicacion



class UbicacionForm(forms.ModelForm):
 class Meta:
        model = Ubicacion
        fields = [
                'pais',
                'departamento',
                'municipio',
                'divisionPolitica',
                'latitud',
                'longitud',
                'especificacionLocacion',
                'cultivada'
            ]
            
        labels = {
                'pais' : 'Pais',
                'departamento' : 'Departamento',
                'municipio' : 'Municipio',
                'divisionPolitica' : 'División politica',
                'latitud' : 'Latitud',
                'longitud' : 'Longitud',
                'especificacionLocacion' : 'Especificación de longitud',
                'cultivada' : '¿Esta cultivada?'
                
        }
        widgets = {
                'pais': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12 ignored'}),
                'departamento': forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12 ignored'}),
                'municipio': forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12 ignored'}),
                'divisionPolitica': forms.TextInput(attrs={'type':'text', 'id':'data_3', 'name':'datepicker', 'class':'form-control col-md-7 col-xs-12 ignored' }),
                'especificacionLocacion' : forms.Textarea(attrs={'class':'form-control col-md-7 col-xs-12  ignored'}),
                'latitud': forms.TextInput(attrs={ 'onkeypress':'return isNumberKey(event)', 'class':'form-control col-md-7 col-xs-12 ignored'}),
                'longitud' : forms.TextInput(attrs={ 'onkeypress':'return isNumberKey(event)', 'class':'form-control col-md-7 col-xs-12 ignored'}),
                'cultivada' : forms.CheckboxInput(attrs={'class':' ignored'}),
        }
        
