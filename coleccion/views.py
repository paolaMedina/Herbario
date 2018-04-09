from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.core.urlresolvers import reverse_lazy
from coleccion.models import Coleccion
from .forms import ColeccionForm
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.forms import ModelForm, inlineformset_factory

# Create your views here.



