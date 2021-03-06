from __future__ import absolute_import, unicode_literals
from nep.celery import app
from django.core.management import call_command
from downloads import views


@app.task()
def rebuild_haystack_index():
    call_command('rebuild_index', verbosity=0, interactive=False)


@app.task()
def build_download_file(experiment_id, template_name):
    views.download_create(experiment_id, template_name)
