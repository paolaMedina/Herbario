
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
from noticia.models import Noticia


@login_required
def Dashboard(request):
    return render(request, 'index.html')


def Home(request):
    noticias = Noticia.objects.all()
    print(noticias)
    contexto = {'noticias': noticias}
    return render(request, 'index-home.html', contexto)
