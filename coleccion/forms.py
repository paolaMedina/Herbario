from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import Coleccion, Colectores
from django.forms import widgets
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings
from cientifico.models import Cientifico
from django.forms.formsets import BaseFormSet

class ColeccionForm(ModelForm):
    class Meta:
        model = Coleccion
        fields = ['fecha','descripcion', ]
                    
                    
        labels = {
                'fecha' : 'Fecha',
                'descripcion' : 'Descripcion',
                
        }
        widgets = {
          
                'fecha': forms.TextInput(attrs={'type':'text', 'id':'data_3', 'name':'datepicker', 'class':'form-control ignored' }),
                'descripcion': forms.Textarea(attrs={'required':'required' , 'class':'form-control ignored'}),

        }


class ColectoresForm(forms.Form):
    
    nombre = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={'class':'form-control nombre-complete','placeholder': 'nombre completo '}),
                    required=False)
                
    abreviatura = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={'class':'form-control'}),
                    )

        



