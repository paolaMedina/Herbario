#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from servicios.models import Servicios

class ServiciosForm(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = [
            'tipo',
            'descripcion',
            'precio',
            'foto',
        ]
        labels = {
            'tipo':'Tipo de servicio',
            'descripcion': 'Descripción',
            'precio':'Valor del servicio',
            'foto':'Fotografia especimen'
        }
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'precio': forms.TextInput(
                attrs={
                    'onkeypress':'isDecimalKey(event,this)',
                    'class':'form-control col-md-7 col-xs-12'
                    }),
            'foto' : forms.ClearableFileInput(
                attrs={
                    'value':'',
                    'class':'form-control col-md-7 col-xs-12'
                }),
        }

class ConsultarServicoForm(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = [
            'ticket'
        ]
        labels = {
            'ticket': 'Número de ticket'
        }
        widgets = {
            'ticket': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'})
        }