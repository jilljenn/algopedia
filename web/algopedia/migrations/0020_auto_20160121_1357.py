# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('algopedia', '0019_auto_20160121_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='implementation',
            name='algo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='algopedia.Algo'),
        ),
    ]
