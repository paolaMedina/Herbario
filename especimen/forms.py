from django import forms
from .models import Especimen



class EspecimenForm(forms.ModelForm):


 class Meta:
        model = Especimen
        fields = [
                'num_registro',
                #'duplicado',
                'lugar_duplicado',
                #'peligro',
                'imagen',

                
            ]
        labels = {
            
                'num_registro' : 'Numero de registro',
                #'duplicado': 'Duplicado',
                'lugar_duplicado' : 'Lugar de duplicado',
                #'peligro': 'Peligro',
                'imagen' : 'Imagen',
                
        }
        widgets = {
                'num_registro': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'numero de registro'}),
                #'duplicado': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'duplicado'}),
                'lugar_duplicado': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'lugar de duplicado'}),
                #'peligro': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'peligro?'}),
               # 'imagen':forms.ImageField(),
               
        }

