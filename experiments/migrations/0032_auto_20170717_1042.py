# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 13:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0031_questionnaireresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='EMGData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('file_format', models.CharField(max_length=50)),
                ('emg_setting_reason_for_change', models.TextField(blank=True, default='', null=True)),
                ('emg_setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.EMGSetting')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.File')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.Participant')),
                ('step', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='experiments.Step')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='eegdata',
            name='eeg_setting_reason_for_change',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
