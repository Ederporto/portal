# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 18:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0002_experimentalprotocol'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='group',
            name='nes_id',
        ),
    ]