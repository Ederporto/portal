# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-30 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0053_emg_settings_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emgelectrodeplacementsetting',
            name='muscle_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='emgelectrodeplacementsetting',
            name='muscle_side',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
