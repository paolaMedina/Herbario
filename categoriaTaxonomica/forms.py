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
                'familia': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12'}),
                'genero': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12'}),
                'epiteto_especifico': forms.TextInput(attrs={'required':'required', 'class':'form-control col-md-7 col-xs-12'}),
                'fecha_det': forms.TextInput(attrs={'type':'text', 'id':'data_3', 'name':'datepicker', 'class':'form-control col-md-7 col-xs-12' }),
                'categoria_infraespecifica': forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12'}),
                'epiteto_infraespecifico' : forms.TextInput(attrs={ 'class':'form-control col-md-7 col-xs-12'}),
                
                

        }
        
