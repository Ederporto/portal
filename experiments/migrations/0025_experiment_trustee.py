# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 15:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experiments', '0024_rejectjustification'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='trustee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experiments', to=settings.AUTH_USER_MODEL),
        ),
    ]
