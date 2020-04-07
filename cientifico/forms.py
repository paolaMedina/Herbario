from django import forms
from cientifico.models import Cientifico



class CientificoForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
                super(CientificoForm, self).__init__(*args, **kwargs)
                self.fields['nombre_completo'].required = False
                self.fields['nombre_abreviado'].required = False

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
                        'nombre_completo': forms.TextInput(attrs={ 'class':'form-control nombre-complete', 'placeholder':'Nombre completo'}),
                        'nombre_abreviado': forms.TextInput(attrs={'class':'form-control','maxlength':30}),


                }
