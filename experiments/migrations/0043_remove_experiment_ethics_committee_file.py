# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 18:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0042_auto_20170720_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='ethics_committee_file',
        ),
    ]
