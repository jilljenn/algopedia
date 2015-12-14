from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from algopedia.models import Algo, Implementation, Category
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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


class ImplementationList(ListView):
    model = Implementation

    def get_context_data(self, **kwargs):
        context = super(ImplementationList, self).get_context_data(**kwargs)
        context = populate_context(context)
        return context


@method_decorator(login_required, name='dispatch')
class ImplementationCreate(CreateView):
    model = Implementation
    fields = ['lang', 'code']

    def get_context_data(self, **kwargs):
        context = super(ImplementationCreate, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['algo'] = get_object_or_404(Algo, pk=self.kwargs['algo'])
        context['categories_current'] = [cat.pk for cat in context['algo'].category.all()]
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.algo = get_object_or_404(Algo, pk=self.kwargs['algo'])
        return super(ImplementationCreate, self).form_valid(form)


class ImplementationDetail(DetailView):
    model = Implementation

    def get_context_data(self, **kwargs):
        context = super(ImplementationDetail, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['categories_current'] = [cat.pk for cat in context['object'].algo.category.all()]
        return context


