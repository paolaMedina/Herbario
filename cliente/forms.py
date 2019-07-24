#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from cliente.models import Cliente



class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre_completo',
            'tipo_identificacion',
            'identificacion',
            'correo',
            'num_contacto',
            'institucion'
        ]
        labels = {
            'nombre_completo':'Nombre completo',
            'tipo_identificacion': 'Tipo de identificación',
            'identificacion':'Número de identificación',
            'correo':'Correo electrónico',
            'num_contacto':'Número telefónico',
            'institucion':'Institución'
        }
        widgets = {
            'nombre_completo': forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12'}),
            'tipo_identificacion': forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'identificacion': forms.TextInput(
                attrs={
                    'onkeypress':'return isNumberKey(event)',
                    'class':'form-control col-md-7 col-xs-12'
                    }),
            'correo': forms.EmailInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'num_contacto': forms.TextInput(
                attrs={
                    'onkeypress':'return isNumberKey(event)',
                    'class':'form-control col-md-7 col-xs-12'
                    }),
            'institucion': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'})
        }
