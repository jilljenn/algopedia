from django.db import models
from django.contrib.auth.models import User


class Algo(models.Model):
    name = models.CharField(max_length=42)
    description = models.TextField()


class Implementation(models.Model):
    user = models.ForeignKey(User)
    algo = models.ForeignKey('Algo')
    code = models.TextField()
