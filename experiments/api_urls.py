from django.conf.urls import url
from experiments import api

urlpatterns = [
    url(r'^experiments/$', api.ExperimentList.as_view(),
        name='api_experiments'),
    url(r'^studies/(?P<pk>[0-9]+)/experiments/$',
        api.ExperimentList.as_view(), name='api_experiments_post'),
    url(r'^studies/$', api.StudyList.as_view(), name='api_studies'),
    url(r'^researchers/$', api.ResearcherList.as_view(),
        name='api_researchers'),
]
