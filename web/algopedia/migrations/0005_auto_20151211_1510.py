# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-11 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algopedia', '0004_auto_20151211_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=42, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=42, unique=True),
        ),
    ]
