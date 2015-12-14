from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from algopedia.models import Algo, Implementation, Category
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def populate_context(context):
    context['categories'] = context.get('categories', Category.objects.annotate(num=Count('algo')).order_by('-num'))
    context['title'] = context.get('title', 'Algopedia')
    return context

class AlgoList(ListView):
    model = Algo

    def get_context_data(self, **kwargs):
        context = super(AlgoList, self).get_context_data(**kwargs)
        context = populate_context(context)
        return context

class AlgoDetail(DetailView):
    model = Algo

    def get_context_data(self, **kwargs):
        context = super(AlgoDetail, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['categories_current'] = [cat.pk for cat in context['object'].category.all()]
        return context

class ImplementationList(ListView):
    model = Implementation

    def get_context_data(self, **kwargs):
        context = super(ImplementationList, self).get_context_data(**kwargs)
        context = populate_context(context)
        return context


class AlgoCreate(CreateView):
    model = Algo
    fields = ['name', 'description']

    def get_context_data(self, **kwargs):
        context = super(AlgoCreate, self).get_context_data(**kwargs)
        context = populate_context(context)
        return context


def categoryDetail(request, pk):
    context = populate_context({})
    context['object_list'] = Algo.objects.filter(category=pk)
    context['categories_current'] = [int(pk)]
    return render(request, 'algopedia/algo_list.html', context)
