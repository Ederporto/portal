# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 13:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0026_auto_20170529_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protocolcomponent',
            name='owner',
        ),
    ]
