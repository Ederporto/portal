# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 12:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0016_auto_20170519_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='study',
        ),
    ]