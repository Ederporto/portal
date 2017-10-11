# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-10 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0067_auto_20171009_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificationofdiseases',
            name='abbreviated_description_en',
            field=models.CharField(max_length=190, null=True),
        ),
        migrations.AddField(
            model_name='classificationofdiseases',
            name='abbreviated_description_pt_br',
            field=models.CharField(max_length=190, null=True),
        ),
        migrations.AddField(
            model_name='classificationofdiseases',
            name='description_en',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='classificationofdiseases',
            name='description_pt_br',
            field=models.CharField(max_length=300, null=True),
        ),
    ]