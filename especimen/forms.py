#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Especimen

# from floppyforms import ClearableFileInput

# class ImageThumbnailFileInput(ClearableFileInput):
#     template_name = 'image_thumbnail.html'

class EspecimenForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
                super(EspecimenForm, self).__init__(*args, **kwargs)
                self.fields['imagen'].required = False


        class Meta:
                model = Especimen
                fields = [
                        'num_registro',
                        'lugar_duplicado',
                        'peligro',
                        'tipo',
                        'imagen',

                        
                ]
                labels = {
                
                        'num_registro' : 'Número de registro',
                        'lugar_duplicado' : 'Lugar de duplicado',
                        'peligro' : "Categoria de amenaza",
                        'tipo' : 'Tipo',
                        'imagen' : 'Imagen',
                        
                }
                widgets = {
                        'num_registro': forms.TextInput(attrs={ 'onkeypress':'return isNumberKey(event)','required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'numero de registro'}),
                        'lugar_duplicado': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'lugar de duplicado', 'value':'CUVC'}),
                        'peligro' : forms.Select(attrs={'class': 'form-control col-sm-2'}),
                        'tipo' : forms.Select(attrs={'class': 'form-control col-sm-2'}),
                        'imagen' : forms.ClearableFileInput(attrs={'value':'','class':'form-control col-md-7 col-xs-12'}),

                } 

        