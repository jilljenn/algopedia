from django.shortcuts import render
from algopedia.models import Algo, Implementation
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class AlgoList(ListView):
    model = Algo


class AlgoDetail(DetailView):
    model = Algo


class ImplementationList(ListView):
    model = Implementation
