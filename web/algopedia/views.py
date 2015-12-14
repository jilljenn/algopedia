from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from algopedia.models import Algo, Implementation, Category
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


def categoryDetail(request, pk):
    context = {}
    context['object_list'] = Algo.objects.filter(category=pk)
    return render(request, 'algopedia/algo_list.html', context)
