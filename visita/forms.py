#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.forms import widgets
from django.conf import settings
from .models import Visita

class VisitaForm(ModelForm):
    class Meta:
        model = Visita
        fields = ['fecha','hora', 'nombre', 'correo', 'telefono','numPersonas','motivo' ]
        labels = {
                
                'fecha':'Fecha',
                'hora':'Hora',
                'nombre':'Nombre completo',
                'correo':'Correo',
                'telefono':'Telefono',
                'numPersonas': 'Número de visitantes',
                'motivo':'Motivo de la visita',
        }
        widgets = {            
                'fecha': forms.TextInput(attrs={'required':'required','type':'text', 'class':'form-control datetimepicker-input' ,'data-target':"#datetimepicker4"}),
                'hora':forms.TextInput(attrs={'required':'required','type':'text', 'class':'form-control datetimepicker-input', 'data-target':"#datetimepicker3"}),
                'nombre':forms.TextInput(attrs={'required':'required','type':'text', 'class':'form-control' }),
                'correo': forms.EmailInput(attrs={'required':'required','class':'form-control' }),
                'telefono':forms.TextInput(attrs={'required':'required','type':'number', 'class':'form-control' }),
                'numPersonas': forms.TextInput(attrs={'required':'required','type':'number', 'class':'form-control' }),
                'motivo': forms.Textarea(attrs={'required':'required' , 'class':'form-control'}),

        }


        



