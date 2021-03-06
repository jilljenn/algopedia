# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 13:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def move_algo(apps, schema_editor):
    Algo = apps.get_model("algopedia", "Algo")
    AlgoVersion = apps.get_model("algopedia", "AlgoVersion")
    for algo in Algo.objects.all():
        version = AlgoVersion(algo=algo, author_id=1, name=algo.name, description=algo.description)
        version.save()
        algo.current = version
        algo.save()
        version.category.add(*algo.category.all())


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('algopedia', '0012_notebook'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgoVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=42)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='algoversion',
            name='algo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='algopedia.Algo'),
        ),
        migrations.AddField(
            model_name='algoversion',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='algo',
            name='current',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_reverse', to='algopedia.AlgoVersion'),
        ),
        migrations.AddField(
            model_name='algoversion',
            name='category',
            field=models.ManyToManyField(blank=True, to='algopedia.Category'),
        ),
        # move data into the new table
        migrations.RunPython(move_algo),
        migrations.RemoveField(
            model_name='algo',
            name='category',
        ),
        migrations.RemoveField(
            model_name='algo',
            name='description',
        ),
        migrations.RemoveField(
            model_name='algo',
            name='name',
        ),
    ]
