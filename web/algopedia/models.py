from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Count, Case, When, Value, IntegerField
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter, LatexFormatter
from pygments.util import ClassNotFound
from pygments.lexers.special import TextLexer

class Category(models.Model):
    name = models.CharField(max_length=42, unique=True)

    def __str__(self):
        return self.name

class Algo(models.Model):
    current = models.OneToOneField('AlgoVersion', blank=True, null=True,\
        related_name="current_reverse")
        # related_name : otherwise it clashes with AlgoVersion.algo

    def _get_name(self):
        return self.current.name # TODO si current=null ?
    name = property(_get_name) # access name with Algo.name

    
    def _get_description(self):
        return self.current.description
    description = property(_get_description) # access description with Algo.description
    
    def _get_category(self):
        return self.current.category
    category = property(_get_category) # access description with Algo.description
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('algopedia:algo-detail', kwargs={'pk': self.pk})


class AlgoVersion(models.Model):
    algo = models.ForeignKey('Algo')
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    # content
    name = models.CharField(max_length=42)
    description = models.TextField()
    category = models.ManyToManyField('Category', blank=True) # TODO m2m long à copier ?

    def __str__(self):
        return self.name + " by " + str(self.author) + " (" + str(self.date) + ")"

class ImplementationManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        """Add field stars_count"""
        return super(ImplementationManager, self).get_queryset(*args, **kwargs).\
            annotate(stars_count=Count(Case(When(star__active=True, then=Value(1)),\
            output_field=IntegerField())))

class Implementation(models.Model):
    objects = ImplementationManager()

    user = models.ForeignKey(User)
    algo = models.ForeignKey('Algo')
    code = models.TextField()
    lang = models.ForeignKey('Language')
    parent = models.ForeignKey('Implementation', blank=True, null=True)
    visible = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('algopedia:implementation-detail', kwargs={'pk': self.pk})

    def get_lexer(self):
        try:
            return get_lexer_by_name(self.lang.name, stripall=True)
        except ClassNotFound:
            try:
                return guess_lexer(self.code)
            except ClassNotFound:
                return TextLexer()

    def get_code(self):
        return highlight(self.code, self.get_lexer(), HtmlFormatter(linenos=True))

    def get_code_tex_linenos(self):
        return highlight(self.code, self.get_lexer(), LatexFormatter(linenos=True)) #, envname='lstlisting'))

    def get_code_tex(self):
        return highlight(self.code, self.get_lexer(), LatexFormatter(linenos=False)) #, envname='lstlisting'))

    def __str__(self):
        return str(self.algo) + " by " + str(self.user) + " in " + str(self.lang) + " (" + str(self.id) + ")"


class Language(models.Model):
    name = models.CharField(max_length=42, unique=True)

    def __str__(self):
        return self.name


class Star(models.Model):
    user = models.ForeignKey(User)
    implementation = models.ForeignKey(Implementation)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user) + " stars " + str(self.implementation)

    class Meta:
        unique_together = ('user', 'implementation')


class Notebook(models.Model):
    """Parameters for notebook generation"""
    user = models.OneToOneField(User)
    title = models.CharField(max_length=256, default="Notebook")
    author = models.CharField(max_length=256, blank=True)
    linenos = models.BooleanField(default=True)
    multicol = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4)
        ])

    def __str__(self):
        return "Notebook of " + str(self.user)
