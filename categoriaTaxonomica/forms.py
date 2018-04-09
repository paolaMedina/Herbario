from django import forms
from .models import CategoriaTaxonomica



class TaxonomiaForm(forms.ModelForm):


 class Meta:
        model = CategoriaTaxonomica
        fields = [
                'familia',
                'genero',
                'epiteto_especifico',
                'fecha_det',
                'categoria_infraespecifica',
                'epiteto_infraespecifico',

                
            ]
        labels = {
                'familia' : 'Familia',
                'genero' : 'Genero',
                'epiteto_especifico': 'Espiteto Especifico' ,
                'fecha_det' : 'Fecha Determinacion',
                'categoria_infraespecifica' : 'Categoria Infraespecifico',
                'epiteto_infraespecifico' : 'Epiteto Infraespecifico',
                
        }
        widgets = {
                'familia': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'familia'}),
                'genero': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'genero'}),
                'epiteto_especifico': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'epiteto especifico'}),
                'fecha_det': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'fecha de determinacion'}),
                'categoria_infraespecifica': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'categoria infraespecifica'}),
                'epiteto_infraespecifico' : forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12', 'placeholder':'epiteto infraespecifico'}),

        }
        
