from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime
import json

from experiments.models import Experiment, Researcher, Study, ProtocolComponent


def create_study(nes_id, owner):
    """
    Create Study model object to be used to test classes below.
    :param nes_id: client nes id
    :param owner: client owner
    :return: 
    """
    researcher = Researcher.objects.create(nes_id=nes_id, owner=owner)
    # TODO: What a strange behavior. Maybe post question in Stackoverflow.
    # When trying to create our_user User instance without username, test
    # doesn't pass. But in the first User instance created (other_user
    # above), without username, test pass.
    return Study.objects.create(
        nes_id=nes_id, start_date=datetime.utcnow(), researcher=researcher,
        owner=owner
    )


def create_experiment(nes_id, owner):
    """
    Create Experiment model object to be used to test classes below.
    :param nes_id: client nes id
    :param owner: client owner 
    :return: 
    """
    study = create_study(nes_id=nes_id, owner=owner)
    return Experiment.objects.create(
            nes_id=nes_id, title='Our title', description='Our description',
            study=study, owner=owner
    )


class ResearcherAPITest(APITestCase):
    base_url = reverse('api_researchers')

    def test_get_returns_all_researchers(self):
        owner = User.objects.create_user(username='lab1')
        researcher1 = Researcher.objects.create(nes_id=1, owner=owner)
        researcher2 = Researcher.objects.create(nes_id=2, owner=owner)

        response = self.client.get(self.base_url)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [
                {
                    'id': researcher1.id,
                    'first_name': researcher1.first_name,
                    'surname': researcher1.surname,
                    'email': researcher1.email,
                    'studies': [],
                    'nes_id': researcher1.nes_id,
                    'owner': researcher1.owner.username
                },
                {
                    'id': researcher2.id,
                    'first_name': researcher2.first_name,
                    'surname': researcher2.surname,
                    'email': researcher2.email,
                    'studies': [],
                    'nes_id': researcher2.nes_id,
                    'owner': researcher2.owner.username
                }
            ]
        )

    def test_POSTing_a_new_researcher(self):
        owner = User.objects.create_user(username='lab1', password='nep-lab1')
        self.client.login(username=owner.username, password='nep-lab1')
        response = self.client.post(
            self.base_url,
            {
                'first_name': 'João',
                'surname': 'das Rosas',
                'email': 'joao@rosas.com',
                'nes_id': 1,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        new_researcher = Researcher.objects.first()
        self.assertEqual(new_researcher.first_name, 'João')


class StudyAPITest(APITestCase):
    base_url = reverse('api_studies')

    def test_get_returns_all_studies(self):
        owner = User.objects.create_user(username='lab1')
        study1 = create_study(nes_id=1, owner=owner)
        study2 = create_study(nes_id=2, owner=owner)
        response = self.client.get(self.base_url)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [
                {
                    'id': study1.id,
                    'title': study1.title,
                    'description': study1.description,
                    'start_date': study1.start_date.strftime('%Y-%m-%d'),
                    'end_date': study1.end_date,
                    'nes_id': study1.nes_id,
                    'researcher': study1.researcher.first_name,
                    'experiments': [],
                    'owner': study1.owner.username
                },
                {
                    'id': study2.id,
                    'title': study2.title,
                    'description': study2.description,
                    'start_date': study2.start_date.strftime('%Y-%m-%d'),
                    'end_date': study2.end_date,
                    'nes_id': study2.nes_id,
                    'researcher': study2.researcher.first_name,
                    'experiments': [],
                    'owner': study1.owner.username
                },
            ]
        )

    def test_POSTing_a_new_study(self):
        owner = User.objects.create_user(username='lab1', password='nep-lab1')
        researcher = Researcher.objects.create(nes_id=1, owner=owner)
        self.client.login(username=owner.username, password='nep-lab1')
        url = reverse('api_studies_post', args=[researcher.id])
        response = self.client.post(
            url,
            {
                'title': 'New study',
                'description': 'Some description',
                'start_date': datetime.utcnow().strftime('%Y-%m-%d'),
                'nes_id': 1
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        new_study = Study.objects.first()
        self.assertEqual(new_study.title, 'New study')

    # TODO: IMPORTANT! Test client can't POST (PUT etc.) to a model without
        # been its owner. This requires adds, at first, an owner to all
        # models, and ensure that only same client can POST to that model.


class ExperimentAPITest(APITestCase):
    base_url = reverse('api_experiments')

    # TODO: This test is following tutorial. Not necessary because is
    # django-rest-framework. By default object returned is json.
    def test_get_returns_json_200(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_all_experiments(self):
        owner = User.objects.create_user(username='lab1')
        experiment1 = create_experiment(nes_id=1, owner=owner)
        experiment2 = create_experiment(nes_id=2, owner=owner)
        response = self.client.get(self.base_url)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [
                {
                    'id': experiment1.id,
                    'title': experiment1.title,
                    'description': experiment1.description,
                    'data_acquisition_done':
                        experiment1.data_acquisition_done,
                    'nes_id': experiment1.nes_id,
                    'study': experiment1.study.title,
                    'owner': experiment1.owner.username,
                    'protocol_components': []
                },
                {
                    'id': experiment2.id,
                    'title': experiment2.title,
                    'description': experiment2.description,
                    'data_acquisition_done':
                        experiment2.data_acquisition_done,
                    'nes_id': experiment2.nes_id,
                    'study': experiment2.study.title,
                    'owner': experiment2.owner.username,
                    'protocol_components': []
                }
            ]
        )

    def test_POSTing_a_new_experiment_to_an_existing_study(self):
        owner = User.objects.create_user(username='lab1', password='nep-lab1')
        study = create_study(nes_id=1, owner=owner)
        self.client.login(username=owner.username, password='nep-lab1')
        url = reverse('api_experiments_post', args=[study.id])
        response = self.client.post(
            url,
            {
                'title': 'New experiment',
                'description': 'Some description',
                'nes_id': 1
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        new_experiment = Experiment.objects.first()
        self.assertEqual(new_experiment.title, 'New experiment')


class ProtocolComponentAPITest(APITestCase):

    def test_get_returns_all_protocolcomponents(self):
        owner = User.objects.create_user(username='lab1')
        experiment = create_experiment(nes_id=1, owner=owner)
        protocol_component1 = ProtocolComponent.objects.create(
            identification='An identification',
            component_type='A component type',
            nes_id=1, experiment=experiment, owner=owner
        )
        protocol_component2 = ProtocolComponent.objects.create(
            identification='Other identification',
            component_type='Other component type',
            nes_id=2, experiment=experiment, owner=owner
        )
        response = self.client.get(reverse('api_protocolcomponents_post'))
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [
                {
                    'id': protocol_component1.id,
                    'identification': protocol_component1.identification,
                    'description': protocol_component1.description,
                    'duration_value': protocol_component1.duration_value,
                    'component_type': protocol_component1.component_type,
                    'nes_id': protocol_component1.nes_id,
                    'experiment': protocol_component1.experiment.title,
                    'owner': protocol_component1.owner.username
                },
                {
                    'id': protocol_component2.id,
                    'identification': protocol_component2.identification,
                    'description': protocol_component2.description,
                    'duration_value': protocol_component2.duration_value,
                    'component_type': protocol_component2.component_type,
                    'nes_id': protocol_component2.nes_id,
                    'experiment': protocol_component2.experiment.title,
                    'owner': protocol_component2.owner.username
                }
            ]
        )

    def test_POSTing_a_new_protocolcomponent_to_an_existing_experiment(self):
        pass


# TODO: os testes de validações ainda não foram implementados.
# Ver:
# http://www.obeythetestinggoat.com/book/appendix_rest_api.html#_data_validation_an_exercise_for_the_reader
