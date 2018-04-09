from django import forms
from cientifico.models import Cientifico



class CientificoForm(forms.ModelForm):


 class Meta:
        model = Cientifico
        fields = [
                'nombre_completo',
                'nombre_abreviado',

                
            ]
        labels = {
                'nombre_completo': 'Nombre Completo',
                'nombre_abreviado' : 'Abreviatura',
                
        }
        widgets = {
                'nombre_completo': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'Nombre completo'}),
                'nombre_abreviado': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12',  'placeholder':'abreviatura'}),


        }
