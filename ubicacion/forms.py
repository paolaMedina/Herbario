#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Ubicacion



class UbicacionForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
                super(UbicacionForm, self).__init__(*args, **kwargs)
                self.fields['pais'].required = False
                self.fields['departamento'].required = False
                self.fields['municipio'].required = False
                self.fields['divisionPolitica'].required = False
                self.fields['especificacionLocacion'].required = False
                self.fields['latitud'].required = False
                self.fields['posicionLat'].required = False
                self.fields['longitud'].required = False
                self.fields['posicionLong'].required = False
                self.fields['alturaMinima'].required = False
                self.fields['alturaMaxima'].required = False
                self.fields['altUni'].required = False
                self.fields['cultivada'].required = False
        class Meta:
                model = Ubicacion
                fields = [
                        'pais',
                        'departamento',
                        'municipio',
                        'divisionPolitica',
                        'especificacionLocacion',
                        'latitud',
                        'posicionLat',
                        'longitud',
                        'posicionLong',
                        'alturaMinima',
                        'alturaMaxima', 
                        'altUni',
                        'cultivada',
                ]
                
                labels = {
                        'pais' : 'País',
                        'departamento' : 'Departamento',
                        'municipio' : 'Municipio',
                        'divisionPolitica' : 'División política menor',
                        'especificacionLocacion' : 'Especificación de localidad',
                        'latitud' : 'Latitud',
                        'posicionLat':'Sentido latitudinal',
                        'longitud' : 'Longitud',
                        'posicionLong':'Sentido longitudinal',
                        'alturaMinima': 'Altura mínima',
                        'alturaMaxima':'Altura máxima',
                        'altUni': 'Unidades',
                        'cultivada' : '¿Es una planta cultivada?'
                }
                widgets = {
                        'pais': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12 ignored'}),
                        'departamento': forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12 ignored'}),
                        'municipio': forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12 ignored'}),
                        'divisionPolitica': forms.TextInput(attrs={'type':'text', 'id':'data_3', 'name':'datepicker', 'class':'form-control col-md-7 col-xs-12 ignored' }),
                        'especificacionLocacion' : forms.Textarea(attrs={'class':'form-control col-md-7 col-xs-12  ignored'}),
                        'latitud': forms.TextInput(attrs={ 'onkeypress':'isDecimalKey(event,this)', 'class':'form-control col-md-7 col-xs-12 ignored'}),
                        'posicionLat':forms.Select(attrs={'class': 'form-control col-sm-2 ignored'}),
                        'longitud' : forms.TextInput(attrs={ 'onkeypress':'return isDecimalKey(event,this)', 'class':'form-control col-md-7 col-xs-12 ignored'}),
                        'posicionLong':forms.Select(attrs={'class': 'form-control col-sm-2 ignored'}),
                        'alturaMinima' : forms.TextInput(attrs={ 'onkeypress':'isDecimalKey(event,this)', 'class':'form-control col-md-7 col-xs-12 ignored'}),
                        'alturaMaxima' : forms.TextInput(attrs={ 'onkeypress':'isDecimalKey(event,this)', 'class':'form-control col-md-7 col-xs-12 ignored'}), 
                        'altUni' : forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12 ignored', 'value':'m'}),
                        'cultivada' : forms.CheckboxInput(attrs={'class':' ignored i-checks'}),
                }
                
