# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-09 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0066_auto_20171009_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classificationofdiseases',
            name='abbreviated_description',
            field=models.CharField(max_length=190),
        ),
    ]
