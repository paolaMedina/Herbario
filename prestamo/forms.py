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
            'tipo': forms.Textarea(attrs={'class': 'form-control col-sm-10'})
        }
