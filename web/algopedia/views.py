from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count, Q
from algopedia.models import Algo, Implementation, Category, Star
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from difflib import HtmlDiff

def populate_context(context):
    context['categories'] = context.get('categories', Category.objects.annotate(num=Count('algo')).order_by('-num'))
    context['title'] = context.get('title', 'Algopedia')
    return context


class AlgoList(ListView):
    model = Algo

    def get_context_data(self, **kwargs):
        context = super(AlgoList, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['title'] += " - algo - list"
        return context

class AlgoDetail(DetailView):
    model = Algo

    def get_context_data(self, **kwargs):
        context = super(AlgoDetail, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['implementations'] = Implementation.objects.filter(algo=self.kwargs['pk']).filter(visible=True).order_by('lang__name')
        context['categories_current'] = context['object'].category.values_list('pk', flat=True)
        context['title'] += " - algo - " + context['object'].name
        if self.request.user.is_authenticated():
            context['stars'] = [star.implementation_id for star in Star.objects.filter(user=self.request.user).filter(implementation__algo__pk=context['object'].pk)]
        return context


class AlgoCreate(CreateView):
    model = Algo
    fields = ['name', 'description']

    def get_context_data(self, **kwargs):
        context = super(AlgoCreate, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['title'] += " - algo - create"
        return context


class CategoryDetail(TemplateView):
    template_name = "algopedia/category_detail.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['category'] = get_object_or_404(Category, pk=pk)
        context['object_list'] = Algo.objects.filter(category=pk)
        context['categories_current'] = [int(pk)]
        context['title'] += " - category - " + context['category'].name
        return context

class CategoryList(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['title'] += " - category - list"
        context['object_list'] = context.get('categories', Category.objects.annotate(num=Count('algo')).order_by('-num'))
        context['algos'] = Algo.objects.all
        return context


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
        context['categories_current'] = context['algo'].category.values_list('pk', flat=True)
        context['title'] += " - implementation - create"
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
        context['title'] += " - implementation - detail"
        context['categories_current'] = context['object'].algo.category.values_list('pk', flat=True)
        if self.request.user.is_authenticated():
            context['starred'] = Star.objects.filter(implementation__pk=context['object'].pk).filter(user=self.request.user).exists()
        return context


def ajaxImplementationDetail(request, pk):
    context = {'object' : get_object_or_404(Implementation, pk=pk)}
    return render(request, 'algopedia/ajax_implementation_detail.html', context)

class ImplementationDiff(TemplateView):
    template_name = "algopedia/implementation_diff.html"

    def get_context_data(self, **kwargs):
        context = super(ImplementationDiff, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['implem1'] = get_object_or_404(Implementation, pk=kwargs['pk1'])
        context['implem2'] = get_object_or_404(Implementation, pk=kwargs['pk2'])
        context['diff'] = HtmlDiff().make_table(context['implem1'].code.split('\n'), context['implem2'].code.split('\n'))
        context['categories_current'] = Algo.objects.filter(Q(pk=context['implem1'].algo_id) | Q(pk=context['implem2'].algo_id)).values_list('pk', flat=True)
        context['title'] += " - implementation - diff"
        return context


class ImplementationEdit(UpdateView):
    model = Implementation
    fields = ['lang', 'code']
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super(ImplementationEdit, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['algo'] = self.get_object().algo
        context['categories_current'] = context['algo'].category.values_list('pk', flat=True)
        context['title'] += " - implementation - edit"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.parent = get_object_or_404(Implementation, pk=form.instance.pk)
        form.instance.pk = None # create a new row
        return super(ImplementationEdit, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class UserStars(TemplateView):
    template_name = "algopedia/user_stars.html"

    def get_context_data(self, **kwargs):
        context = super(UserStars, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['title'] += " - stars"
        req = Star.objects.filter(user=self.request.user)
        context['stars'] = req.filter(active=True)
        context['stars_old'] = req.filter(active=False)
        return context

class Index(TemplateView):
    template_name = "algopedia/index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['title'] += " - index"
        return context
