from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    username=forms.CharField(required=True,label='Nombre Usuario')
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellidos')
    email = forms.EmailField(required=True, label= 'Correo Electronico',widget=forms.TextInput(attrs={'type':'email', 'class':'form-control', 'required':'required'}))
    password1 = forms.CharField(required=True, label='Contrasena')
    password2 = forms.CharField(required=True, label='Confirmacion contrasena')

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')
      