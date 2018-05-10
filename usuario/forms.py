from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#Importamos el formulario de autenticacion de django
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    username=forms.CharField(required=True,label='Nombre Usuario',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    first_name = forms.CharField(required=True, label='Nombres',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    last_name = forms.CharField(required=True, label='Apellidos',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    email = forms.EmailField(required=True, label= 'Correo Electronico',widget=forms.EmailInput(attrs={'type':'email', 'class':'form-control', 'required':'required'}))
    password1 = forms.CharField(required=True, label='Contrasena',widget=forms.PasswordInput(attrs={'class':'form-control example1','id':"password" ,'required':'required'}))
    password2 = forms.CharField(required=True, label='Confirmacion contrasena',widget=forms.PasswordInput(attrs={'class':'form-control','id':"password_again", 'required':'required'}))
 
    class Meta:
        model = Usuario
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2','rol','identificacion')
        
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-control col-sm-2'}),
            'identificacion': forms.TextInput(attrs={ 'onkeypress':'return isNumberKey(event)','required':'required', 'class':'form-control col-md-7 col-xs-12'}),
           }
           



class FormularioLogin(AuthenticationForm):

    def __init__(self, *args, **kwargs):
            super(FormularioLogin, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
            self.fields['password'].widget.attrs['class'] = 'form-control'
            self.fields['password'].widget.attrs['placeholder'] = 'Contrasena'
            
class FormularioReset(PasswordResetForm):
    def __init__(self, *args, **kwargs):
            super(FormularioReset, self).__init__(*args, **kwargs)
            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['placeholder'] = 'Usuario'