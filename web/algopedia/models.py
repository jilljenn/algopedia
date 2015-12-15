from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
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

    def get_absolute_url(self):
       return reverse('algopedia:implementation-detail', kwargs={'pk': self.pk})

    def get_code(self):
       try:
           lexer = get_lexer_by_name(self.lang.name, stripall=True)
       except ClassNotFound:
           try:
               lexer = guess_lexer(self.code)
           except ClassNotFound:
               lexer = TextLexer()
       formatter = HtmlFormatter(linenos=True)
       return highlight(self.code, lexer, formatter)


class Language(models.Model):
    name = models.CharField(max_length=42, unique=True)

    def __str__(self):
        return self.name
