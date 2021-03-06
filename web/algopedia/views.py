from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.db import transaction
from django.db.models import Count, Q, F, Case, When, IntegerField, Value
from algopedia.models import Algo, AlgoVersion, Implementation, Category, Star, Notebook
from django.views.generic import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from difflib import HtmlDiff
from algopedia.notebook import generatePdf, generateTex
import os
from shutil import copyfileobj

def populate_context(context):
    # TODO fonctionne PAS
    context['categories'] = context.get('categories', Category.objects.annotate(num=Count('algoversion__algo__current')).order_by('-num'))
    context['title'] = context.get('title', 'Algopedia')
    return context


def stars_list(stars):
    return [star.implementation_id for star in stars]


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
        context['implementations'] = Implementation.objects.filter(algo=self.kwargs['pk']).filter(visible=True).order_by('lang__name', '-stars_count')
        context['categories_current'] = context['object'].category.values_list('pk', flat=True)
        context['title'] += " - algo - " + context['object'].name
        if 'revision' in self.kwargs:
            # we change current revision for display
            context['object'].current = get_object_or_404(AlgoVersion, pk=self.kwargs['revision'])
            if context['object'].current.algo_id != context['object'].pk:
                raise Http404
        if self.request.user.is_authenticated():
            context['stars'] = stars_list(Star.objects.filter(user=self.request.user, implementation__algo_id=context['object'].pk, active=True))
        return context


@method_decorator(login_required, name='dispatch')
class AlgoEdit(UpdateView):
    model = AlgoVersion
    fields = ['name', 'description', 'category']
    template_name = 'algopedia/algo_form.html'

    def get_context_data(self, **kwargs):
        context = super(AlgoEdit, self).get_context_data(**kwargs)
        context = populate_context(context)
        algoVersion = self.get_object()
        context['categories_current'] = algoVersion.category.values_list('pk', flat=True)
        context['title'] += " - algo - edit"
        context['form_title'] = "Edit " + algoVersion.name
        return context

    # atomic : algo.current is updated simultaeneously
    @transaction.atomic
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pk = None # create a new row
        form.save()
        # update algo.current
        form.instance.algo.current = form.instance
        form.instance.algo.save()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class AlgoCreate(CreateView):
    model = AlgoVersion
    fields = ['name', 'description', 'category']
    template_name = 'algopedia/algo_form.html'

    def get_context_data(self, **kwargs):
        context = super(AlgoCreate, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['title'] += " - algo - create"
        context['form_title'] = "Create the description of an algorithm"
        return context

    # atomic : create algo and algoVersion simultaeneously
    @transaction.atomic
    def form_valid(self, form):
        algo = Algo()
        algo.save()
        form.instance.author = self.request.user
        form.instance.algo = algo
        form.save()
        algo.current = form.instance
        algo.save()
        return HttpResponseRedirect(form.instance.get_absolute_url())


class AlgoHistory(TemplateView):
    template_name = "algopedia/algo_history.html"

    def get_context_data(self, **kwargs):
        context = super(AlgoHistory, self).get_context_data(**kwargs)
        context = populate_context(context)
        pk = self.kwargs['pk']
        context['object'] = get_object_or_404(Algo, pk=pk)
        context['object_list'] = AlgoVersion.objects.filter(algo_id=pk).order_by('-date')
        context['categories_current'] = context['object'].category.values_list('pk', flat=True)
        context['title'] += " - algo - history"
        return context


class CategoryDetail(TemplateView):
    template_name = "algopedia/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context = populate_context(context)
        pk = self.kwargs['pk']
        context['category'] = get_object_or_404(Category, pk=pk)
        context['object_list'] = Algo.objects.filter(current__category=pk)
        context['categories_current'] = [int(pk)]
        context['title'] += " - category - " + context['category'].name
        return context

class CategoryList(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['title'] += " - category - list"
        return context

    def get_queryset(self):
        # TODO fonctionne PAS
        return Category.objects.annotate(num=Count('algoversion__algo__current')).order_by('-num')



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
        context['children'] = Implementation.objects.filter(parent_id=context['object'])
        if self.request.user.is_authenticated():
            context['stars'] = stars_list(Star.objects\
                .filter(user=self.request.user, active=True)\
                .filter(Q(implementation__parent_id=context['object'].pk)\
                  | Q(implementation_id=context['object'].pk)))
        return context


class ImplementationDetailAjax(View):
    def get(self, request, *args, **kwargs):
        context = {'object' : get_object_or_404(Implementation, pk=kwargs['pk'])}
        if self.request.user.is_authenticated():
            context['stars'] = stars_list(Star.objects.filter(implementation_id=kwargs['pk'], user=self.request.user, active=True))
        return render(request, 'algopedia/ajax_implementation_detail.html', context)

def starAddRemove(action, user, implem):
    if action == 'add':
        Star.objects.update_or_create(defaults={'active':True}, implementation_id=implem, user=user)
    else:
        star = get_object_or_404(Star, implementation_id=implem, user=user)
        star.active = False
        star.save()

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class StarAjax(View):
    def get(self, request, *args, **kwargs):
        starAddRemove(kwargs['action'], request.user, kwargs['pk'])
        stars_count = get_object_or_404(Implementation, pk=kwargs['pk']).stars_count
        return JsonResponse({'status':'ok', 'stars_count':stars_count})

class StarRedirect(View):
    def get(self, request, *args, **kwargs):
        starAddRemove(kwargs['action'], request.user, kwargs['pk'])
        return redirect(request.GET.get('next', '/'))


class ImplementationDiff(TemplateView):
    template_name = "algopedia/implementation_diff.html"

    def get_context_data(self, **kwargs):
        context = super(ImplementationDiff, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['implem1'] = get_object_or_404(Implementation, pk=kwargs['pk1'])
        context['implem2'] = get_object_or_404(Implementation, pk=kwargs['pk2'])
        if context['implem1'].algo.pk != context['implem2'].algo.pk:
            raise Http404
        if self.request.user.is_authenticated():
            context['stars'] = stars_list(Star.objects\
                .filter(user=self.request.user, active=True)\
                .filter(Q(implementation_id=kwargs['pk1']) | Q(implementation_id=kwargs['pk2'])))
        context['diff'] = HtmlDiff().make_table(context['implem1'].code.split('\n'), context['implem2'].code.split('\n'))
        context['categories_current'] = context['implem1'].algo.category.values_list('pk', flat=True)
        context['title'] += " - implementation - diff"
        return context


@method_decorator(login_required, name='dispatch')
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

    # atomic : the parent is hidden and the child is created simultaeneously
    @transaction.atomic
    def form_valid(self, form):
        form.instance.user = self.request.user
        parent = get_object_or_404(Implementation, pk=form.instance.pk)
        if(parent.user == self.request.user): # hide old implementation # TODO prévenir les gens qui ont forké ou starré le code qu'il y a une maj
            parent.visible = False
            parent.save()
        form.instance.parent = parent
        form.instance.pk = None # create a new row
        return super(ImplementationEdit, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class UserProfile(TemplateView):
    template_name = "algopedia/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['title'] += " - profile"

        # stars
        # edited : implementation__implementation refers to children (parent reverse relation)
        # we want to see if the same author has edited his implementation
        req = Star.objects.filter(user=self.request.user)\
            .annotate(edited=Count(Case(When(implementation__implementation__user=F('implementation__user'), then=Value(1)),\
            output_field=IntegerField())))

        context['stars_active'] = req.filter(active=True)
        context['stars_old'] = req.filter(active=False)

        # implementations
        context['implementations'] = Implementation.objects.filter(user=self.request.user)\
            .order_by('algo__current__name')
        context['stars'] = stars_list(context['stars_active'])

        return context


class Index(TemplateView):
    template_name = "algopedia/index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context = populate_context(context)
        context['title'] += " - index"
        return context


@method_decorator(login_required, name='dispatch')
class NotebookParams(UpdateView):
    model = Notebook
    fields = ['title', 'author', 'linenos', 'multicol']

    def get_object(self, queryset=None):
        """Create a new row if it does not exist"""
        # we do not use get_or_create because it commit the new object to the DB
        try:
          obj = Notebook.objects.get(user=self.request.user)
        except Notebook.DoesNotExist:
          obj = Notebook(user=self.request.user)
        return obj

    def get_success_url(self):
        if 'pdf' in self.request.POST:
            return reverse('algopedia:user-notebook-gen', kwargs={'format':'pdf'})
        elif 'tex' in self.request.POST:
            return reverse('algopedia:user-notebook-gen', kwargs={'format':'tex'})
        return reverse('algopedia:user-notebook')


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class NotebookGen(View):
    def get(self, request, *args, **kwargs):
        params = get_object_or_404(Notebook, user=self.request.user)
        implementations = Star.objects.filter(user=self.request.user, active=True)\
            .order_by('implementation__algo__current__name')
        if kwargs['format'] == 'tex':
            latex = generateTex(implementations, params)
            return HttpResponse(latex, content_type="application/x-tex")
        else: # pdf
            pdffilename = generatePdf(implementations, params)
            pdffile = open(pdffilename, 'rb')
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="notebook.pdf"'
            copyfileobj(pdffile, response)
            # delete pdf
            pdffile.close()
            os.remove(pdffilename)
            return response
