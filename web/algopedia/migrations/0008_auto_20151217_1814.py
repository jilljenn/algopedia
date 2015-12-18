# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 18:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('algopedia', '0007_star'),
    ]

    operations = [
        migrations.AddField(
            model_name='implementation',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 12, 17, 18, 14, 37, 331009, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='implementation',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='algopedia.Implementation'),
        ),
    ]