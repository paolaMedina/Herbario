from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    """
    username=forms.CharField(required=True,label='Nombre Usuario',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    first_name = forms.CharField(required=True, label='Nombres',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    last_name = forms.CharField(required=True, label='Apellidos',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    email = forms.EmailField(required=True, label= 'Correo Electronico',widget=forms.EmailInput(attrs={'type':'email', 'class':'form-control', 'required':'required'}))
    password1 = forms.CharField(required=True, label='Contrasena',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    password2 = forms.CharField(required=True, label='Confirmacion contrasena',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    """
    class Meta:
        model = Usuario
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2','rol')
        label ={
            'username':'Nombres',
            'first_name':'Apellidos', 
            'last_name':'Correo Electronico', 
            'email':'Correo Electronico', 
            'password1':'Contrasena', 
            'password2':'Confirmacion contrasena',
            'rol':'rol'
        }
        widgets = {
           'username': forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'required':'required'}),
            'email': forms.EmailInput(attrs={'type':'email', 'class':'form-control', 'required':'required'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control', 'required':'required'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control', 'required':'required'}),
            'rol': forms.Select(attrs={'class': 'form-control col-sm-2'}),
           
           }