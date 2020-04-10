#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(NoticiaForm, self).__init__(*args, **kwargs)
            self.fields['imagen'].required = False


    class Meta:
        model = Noticia
        fields = [
            'titulo',
            'resumen',
            'contenido',
            'imagen',
        ]
        labels = {
            'titulo' : 'Titulo',
            'resumen' : 'Resumen',
            'contenido' : 'Contenido',
            'imagen' : 'Imagen'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'required':'required', 'class':'form-control'}),
            'resumen': forms.Textarea(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12'}),
            'contenido' : forms.Textarea(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12'}),
            'imagen' : forms.ClearableFileInput(attrs={'value':'','class':'form-control col-md-7 col-xs-12'}),
        } 

        