#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.forms import widgets
import datetime
from django.conf import settings
from .models import Visita

class VisitaForm(ModelForm):
    class Meta:
        model = Visita
        fields = ['fecha','hora', 'nombre', 'correo', 'telefono','numPersonas','motivo' ]
        labels = {
                
                'fecha':'Fecha',
                'hora':'Hora',
                'nombre':'Nombre',
                'correo':'Correo',
                'telefono':'Telefono',
                'numPersonas': 'Número de visitantes',
                'motivo':'Motivo de la visita',
        }
        widgets = {            
                'fecha': forms.TextInput(attrs={'required':'required','type':'text', 'id':'data', 'name':'datepicker', 'class':'form-control' }),
                'hora':forms.TimeField(
        widget=TimePicker(
            options={
                'enabledHours': [9, 10, 11, 12, 13, 14, 15, 16],
            },
            attrs={
                'input_toggle': True,
                'input_group': False,
            },
        ),
    ),
                
                
                # forms.TextInput(attrs={'required':'required','type':'text', 'id':'time', 'class':'form-control' }),
                'nombre':forms.TextInput(attrs={'required':'required','type':'text', 'class':'form-control' }),
                'correo': forms.EmailInput(attrs={'required':'required','class':'form-control' }),
                'telefono':forms.TextInput(attrs={'required':'required','type':'number', 'class':'form-control' }),
                'numPersonas': forms.TextInput(attrs={'required':'required','type':'number', 'class':'form-control' }),
                'motivo': forms.Textarea(attrs={'required':'required' , 'class':'form-control'}),

        }


        



