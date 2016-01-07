from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
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
    name = models.CharField(max_length=42)
    description = models.TextField()
    category = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('algopedia:algo-detail', kwargs={'pk': self.pk})


class Implementation(models.Model):
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
        return str(self.algo) + " by " + str(self.user) + " in " + str(self.lang)


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
