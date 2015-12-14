from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

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


class Language(models.Model):
    name = models.CharField(max_length=42, unique=True)

    def __str__(self):
        return self.name
