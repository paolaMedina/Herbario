#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.forms import widgets
from django.conf import settings
from .models import Visita


# class DateForm(forms.Form):
#     fecha = forms.DateTimeField(
#         input_formats=['%m/%d/%Y'],
#         widget=forms.DateTimeInput(attrs={
#             'class': 'form-control datetimepicker-input',
#             'data-target': '#datetimepicker1'
#         })
#     )


class VisitaForm(ModelForm):

    class Meta:
        model = Visita
        fields = ['fecha', 'hora', 'nombre', 'correo',
                  'telefono', 'numPersonas', 'motivo']
        labels = {

            'fecha': 'Fecha',
            'hora': 'Hora',
            'nombre': 'Nombre completo',
            'correo': 'Correo',
            'telefono': 'Telefono',
            'numPersonas': 'Número de visitantes',
            'motivo': 'Motivo de la visita',
        }
        widgets = {
            'fecha': forms.TextInput(attrs={'required': 'required', 'type': 'text', 'class': 'form-control datetimepicker-input', 'data-target': "#datetimepicker4"}),
            'hora': forms.TextInput(attrs={'required': 'required', 'type': 'text', 'class': 'form-control datetimepicker-input', 'data-target': "#datetimepicker3"}),
            'nombre': forms.TextInput(attrs={'required': 'required', 'type': 'text', 'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'required': 'required', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'required': 'required', 'type': 'text', 'class': 'form-control', 'onkeypress':'return isNumberKey(event)'}),
            'numPersonas': forms.TextInput(attrs={'required': 'required', 'type': 'number', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'required': 'required', 'class': 'form-control'}),

        }
