# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0023_merge_20170703_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='RejectJustification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=500)),
                ('experiment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='justification', to='experiments.Experiment')),
            ],
        ),
    ]
