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
                'fecha': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12' }),
                'descripcion': forms.Textarea(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12' }),

        }


class ColectoresForm(forms.Form):
    
    nombre = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'nombre ',
                    }),
                    required=True)
                
    abreviatura = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'abreviatura ',
                    }),
                    required=True)
                    
    orden =  forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'orden ',
                    }),
                    required=True)
    
        



class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        nombres = []
        abreviaturas = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                nombre = form.cleaned_data['nombre']
                abreviatura = form.cleaned_data['abreviatura']

                # Check that no two links have the same anchor or URL
                if nombre and abreviatura:
                    if abreviatura in nombres:
                        duplicates = True
                    nombres.append(nombre)

                    if abreviatura in abreviaturas:
                        duplicates = True
                    abreviaturas.append(abreviatura)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique anchors and URLs.',
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if abreviatura and not nombre:
                    raise forms.ValidationError(
                        'All links must have an anchor.',
                        code='missing_anchor'
                    )
                elif nombre and not abreviatura:
                    raise forms.ValidationError(
                        'All links must have a URL.',
                        code='missing_URL'
                    )
        
