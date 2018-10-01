# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.core.exceptions import ValidationError

class FormUpload(forms.Form):
    file = forms.FileField( )
    
    