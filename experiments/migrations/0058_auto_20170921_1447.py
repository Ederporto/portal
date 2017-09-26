# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-21 17:47
from __future__ import unicode_literals

from django.db import migrations
from django.template.defaultfilters import slugify


def create_slug(apps, schema_editor):
    Experiment = apps.get_model('experiments', 'Experiment')
    for experiment in Experiment.objects.all():
        count = Experiment.objects.filter(
            slug__startswith=slugify(experiment.title)
        ).count()
        # if there're slugs that starts with same name, adds 1 to
        # count to save as unique slug
        if count > 0:
            experiment.slug = slugify(experiment.title + '-' + str(count+1))
        else:
            experiment.slug = slugify(experiment.title)
        experiment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0057_experiment_slug'),
    ]

    operations = [
        migrations.RunPython(create_slug),
    ]
