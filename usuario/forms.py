# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#Importamos el formulario de autenticacion de django
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .models import Usuario



class RegistroForm(forms.ModelForm):
    
   #recibe el grupo del usuario que envia desde la vista  y si es un curador, se restringe el campo rol ya que este solo puede crear monitores
    def __init__(self, groups, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        if groups[0]=='curador':  
            self.fields['rol'].widget.attrs['readonly'] = True
        else:
           self.fields['rol'].widget.attrs['disabled'] = False
    
    username=forms.CharField(required=True,label='Nombre Usuario',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    first_name = forms.CharField(required=True, label='Nombres',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    last_name = forms.CharField(required=True, label='Apellidos',widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
    email = forms.EmailField(required=True, label= 'Correo Electrónico',widget=forms.EmailInput(attrs={'type':'email', 'class':'form-control', 'required':'required'}))
 
    
    class Meta:
        model = Usuario
        fields = ('username','first_name', 'last_name', 'email','rol','identificacion')
        
        labels = {
            
                'rol' : 'Rol',
                'identificacion' : 'Identificación',
        }
        
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-control col-sm-2'}),
            'identificacion': forms.TextInput(attrs={ 'onkeypress':'return isNumberKey(event)','required':'required', 'class':'form-control col-md-7 col-xs-12'}),
           }
           
           
    #clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Este email ya se encuentra registrado')
  
  
class FormularioLogin(AuthenticationForm):

    def __init__(self, *args, **kwargs):
            super(FormularioLogin, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
            self.fields['password'].widget.attrs['class'] = 'form-control'
            self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
            
class FormularioReset(PasswordResetForm):
    def __init__(self, *args, **kwargs):
            super(FormularioReset, self).__init__(*args, **kwargs)
            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['placeholder'] = 'Usuario'