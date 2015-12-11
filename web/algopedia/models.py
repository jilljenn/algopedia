from django.db import models
from django.contrib.auth.models import User


class Algo(models.Model):
    name = models.CharField(max_length=42)
    description = models.TextField()

    def __str__(self):
        return self.name


class Implementation(models.Model):
    user = models.ForeignKey(User)
    algo = models.ForeignKey('Algo')
    code = models.TextField()
    lang = models.ForeignKey('Language')


class Language(models.Model):
    name = models.CharField(max_length=42)

    def __str__(self):
        return self.name