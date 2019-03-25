
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators  import  login_required
from django.views.defaults import page_not_found

@login_required
def Dashboard(request):
    return render(request, 'index.html')
    
def Home(request):
    return render(request, 'index-home.html')
    