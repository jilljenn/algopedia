# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-19 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algopedia', '0008_auto_20151217_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='star',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]