# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-05 11:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0003_auto_20170602_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('study', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='experiments.Study')),
            ],
        ),
    ]
