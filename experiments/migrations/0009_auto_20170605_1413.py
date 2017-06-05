# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-05 17:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0008_auto_20170605_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborator',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='collaborator',
            name='study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborators', to='experiments.Study'),
        ),
        migrations.AlterField(
            model_name='collaborator',
            name='team',
            field=models.CharField(max_length=200),
        ),
    ]
