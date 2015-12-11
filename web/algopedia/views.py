from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from algopedia.models import Algo, Implementation
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class AlgoList(ListView):
    model = Algo


class AlgoDetail(DetailView):
    model = Algo


class ImplementationList(ListView):
    model = Implementation


class AlgoCreate(CreateView):
    model = Algo
    fields = ['name', 'description']
