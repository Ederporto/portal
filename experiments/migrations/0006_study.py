# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0005_experiment_data_acquisition_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=150)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
            ],
        ),
    ]