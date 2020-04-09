#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from prestamo.models import Prestamo

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            'solicitud'
        ]
        labels = {
            'solicitud':'Solicitud',
        }
        widgets = {
            'solicitud': forms.Textarea(attrs={'class': 'form-control col-sm-7'})
        }

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            'solicitud',
            'num_registro' ,
            'fecha_devolucion',
            'observaciones_entrega',
        ]
        labels = {
            'solicitud': "Solicitud",
            'num_registro': 'Número de registro especimen' ,
            'fecha_devolucion': 'Fecha devolución',
            'observaciones_entrega' : 'Obeservaciones de entrega',
        }
        widgets = {
            'solicitud': forms.Textarea(attrs={'class': 'form-control col-sm-7'}),
            'fecha_devolucion': forms.TextInput(attrs={'type':'text','required':'required', 'id':'data_3', 'name':'datepicker', 'class':'form-control' }),
            'num_registro': forms.TextInput(attrs={ 'onkeypress':'return isNumberKey(event)','required':'required', 'class':'form-control col-md-7 col-xs-12'}),
            'observaciones_entrega': forms.Textarea(attrs={'class': 'form-control col-sm-7'})
        }