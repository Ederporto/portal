# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-31 18:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0054_emg_electrode_placement_muscle_nullable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmsdevicesetting',
            name='coil_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tms_device_settings', to='experiments.CoilModel'),
        ),
        migrations.AlterField(
            model_name='tmsdevicesetting',
            name='tms_device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tms_device_settings', to='experiments.TMSDevice'),
        ),
    ]
