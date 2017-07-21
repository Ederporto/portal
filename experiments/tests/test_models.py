from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import datetime

from experiments.models import Experiment, Study, Group, Researcher, \
    Collaborator, RejectJustification, EthicsCommitteeInfo
from experiments.tests.tests_helper import global_setup_ut, apply_setup, \
    create_experiment


@apply_setup(global_setup_ut)
class ResearcherModelTest(TestCase):

    def setUp(self):
        global_setup_ut()

    def test_default_attributes(self):
        researcher = Researcher()
        self.assertEqual(researcher.name, '')
        self.assertEqual(researcher.email, '')

    def test_researcher_is_related_to_one_study(self):
        study = Study.objects.last()
        researcher = Researcher(study=study)
        researcher.save()
        self.assertEqual(researcher, study.researcher)

    def test_cannot_save_empty_attributes(self):
        researcher = Researcher(study=Study.objects.first())
        with self.assertRaises(ValidationError):
            researcher.full_clean()

    # TODO: cannot save researcher without study


@apply_setup(global_setup_ut)
class StudyModelTest(TestCase):

    def setUp(self):
        global_setup_ut()

    def test_default_attributes(self):
        study = Study()
        self.assertEqual(study.title, '')
        self.assertEqual(study.description, '')
        self.assertEqual(study.start_date, None)
        self.assertEqual(study.end_date, None)

    def test_cannot_save_empty_attributes(self):
        study = Study(title='', description='', start_date='')
        with self.assertRaises(ValidationError):
            study.save()
            study.full_clean()

    def test_study_has_only_one_experiment(self):
        # Valid because in tests_helper.py we are creating experiments tied
        # with studies
        experiment = Experiment.objects.last()
        study = Study(start_date=datetime.utcnow(),
                      experiment=experiment)
        with self.assertRaises(ValidationError):
            study.full_clean()


@apply_setup(global_setup_ut)
class EthicsCommitteInfoModelTest(TestCase):

    def setUp(self):
        global_setup_ut()

    def test_default_attributes(self):
        ethics_committe_info = EthicsCommitteeInfo()
        self.assertEqual(ethics_committe_info.project_url, None)
        self.assertEqual(ethics_committe_info.ethics_committee_url, '')
        self.assertEqual(ethics_committe_info.file, '')

    def test_cannot_save_empty_attributes(self):
        owner = User.objects.first()
        create_experiment(1, owner, Experiment.TO_BE_ANALYSED)
        experiment = Experiment.objects.last()
        ethics_committe_info = EthicsCommitteeInfo(
            ethics_committee_url='', file='', experiment=experiment
        )
        with self.assertRaises(ValidationError):
            ethics_committe_info.save()
            ethics_committe_info.full_clean()

    def test_ethics_committee_info_has_only_one_experiment(self):
        experiment = Experiment.objects.first()
        ethics_committe_info = EthicsCommitteeInfo(
            ethics_committee_url='http://example.com', experiment=experiment
        )
        with self.assertRaises(ValidationError):
            ethics_committe_info.full_clean()


@apply_setup(global_setup_ut)
class ExperimentModelTest(TestCase):

    def setUp(self):
        global_setup_ut()

    def test_default_attributes(self):
        experiment = Experiment()
        self.assertEqual(experiment.nes_id, None)
        self.assertEqual(experiment.title, '')
        self.assertEqual(experiment.description, '')
        self.assertEqual(experiment.data_acquisition_done, False)
        self.assertEqual(experiment.sent_date, None)
        self.assertEqual(experiment.version, None)
        self.assertEqual(experiment.status, experiment.RECEIVING)
        self.assertEqual(experiment.trustee, None)

    def test_cannot_save_empty_attributes(self):
        owner = User.objects.first()
        # version=17: large number to avoid conflicts with global setup
        experiment = Experiment(
            nes_id=1, title='', description='', owner=owner,
            version=17, sent_date=datetime.utcnow()
        )
        with self.assertRaises(ValidationError):
            experiment.save()
            experiment.full_clean()

    def test_duplicate_experiments_are_invalid(self):
        owner = User.objects.first()
        Experiment.objects.create(nes_id=17, owner=owner,
                                  version=1, sent_date=datetime.utcnow())
        experiment = Experiment(nes_id=17, owner=owner,
                                version=1, sent_date=datetime.utcnow())
        with self.assertRaises(ValidationError):
            experiment.full_clean()

    def test_CAN_save_same_experiment_to_different_owners(self):
        owner1 = User.objects.get(username='lab1')
        owner2 = User.objects.get(username='lab2')
        Experiment.objects.create(
            title='A title', description='A description', nes_id=1,
            owner=owner1, version=17,
            sent_date=datetime.utcnow()
        )
        experiment2 = Experiment(title='A title', description='A description',
                                 nes_id=1, owner=owner2,
                                 version=17,
                                 sent_date=datetime.utcnow())
        experiment2.full_clean()

    def test_experiment_is_related_to_owner(self):
        owner = User.objects.first()
        experiment = Experiment(nes_id=17, owner=owner,
                                version=1, sent_date=datetime.utcnow())
        experiment.save()
        self.assertIn(experiment, owner.experiment_set.all())


# @apply_setup(global_setup_ut)
# class ProtocolComponentModelTest(TestCase):
#
#     def setUp(self):
#         global_setup_ut()
#
#     def test_default_attributes(self):
#         protocol_component = ProtocolComponent()
#         self.assertEqual(protocol_component.identification, '')
#         self.assertEqual(protocol_component.description, '')
#         self.assertEqual(protocol_component.duration_value, None)
#         self.assertEqual(protocol_component.component_type, '')
#         self.assertEqual(protocol_component.nes_id, None)
#
#     def test_protocol_component_is_related_to_experiment_and_owner(self):
#         owner = User.objects.first()
#         experiment = Experiment.objects.first()
#         protocolcomponent = ProtocolComponent(
#             identification='An identification',
#             component_type='A component type',
#             nes_id=1, experiment=experiment, owner=owner
#         )
#         protocolcomponent.save()
#         self.assertIn(protocolcomponent, experiment.protocol_components.all())
#         self.assertIn(protocolcomponent, owner.protocolcomponent_set.all())
#
#     def test_cannot_save_empty_attributes(self):
#         owner = User.objects.last()
#         experiment = Experiment.objects.first()
#         protocol_component = ProtocolComponent(
#             identification='', component_type='', nes_id=1,
#             experiment=experiment, owner=owner
#         )
#         with self.assertRaises(ValidationError):
#             protocol_component.save()
#             protocol_component.full_clean()
#
#     def test_duplicate_protocol_components_are_invalid(self):
#         owner = User.objects.last()
#         experiment = Experiment.objects.first()
#         ProtocolComponent.objects.create(nes_id=1, experiment=experiment,
#                                          owner=owner)
#         protocol_component = ProtocolComponent(
#             nes_id=1, identification='An identification',
#             duration_value=10, component_type='A component type',
#             experiment=experiment, owner=owner
#         )
#         with self.assertRaises(ValidationError):
#             protocol_component.full_clean()
#
#     def test_CAN_save_same_protocol_components_to_different_owners(self):
#         owner1 = User.objects.get(username='lab1')
#         owner2 = User.objects.get(username='lab2')
#         experiment1 = Experiment.objects.get(owner=owner1)
#         experiment2 = Experiment.objects.get(owner=owner2)
#         ProtocolComponent.objects.create(
#             nes_id=1, experiment=experiment1, owner=owner1
#         )
#         protocol_component = ProtocolComponent(
#             nes_id=1, identification='An identification',
#             duration_value=10, component_type='A component type',
#             experiment=experiment2, owner=owner2,
#         )
#         protocol_component.full_clean()


@apply_setup(global_setup_ut)
class GroupModelTest(TestCase):

    def setUp(self):
        global_setup_ut()

    def test_default_attributes(self):
        group = Group()
        self.assertEqual(group.title, '')
        self.assertEqual(group.description, '')

    def test_group_is_related_to_experiment(self):
        experiment = Experiment.objects.first()
        group = Group.objects.create(
            title='Group A', description='A description',
            experiment=experiment
        )
        self.assertIn(group, experiment.groups.all())

    def test_cannot_save_empty_attributes(self):
        experiment = Experiment.objects.first()
        group = Group.objects.create(
            title='', description='',
            experiment=experiment
        )
        with self.assertRaises(ValidationError):
            group.save()
            group.full_clean()


@apply_setup(global_setup_ut)
class CollaboratorModel(TestCase):

    def setUp(self):
        global_setup_ut()

    def test_default_attributes(self):
        collaborator = Collaborator()
        self.assertEqual(collaborator.name, '')
        self.assertEqual(collaborator.team, '')
        self.assertEqual(collaborator.coordinator, False)

    def test_collaborator_is_related_to_study(self):
        study = Study.objects.first()
        collaborator = Collaborator.objects.create(
            name='Joãzinho trinta', team='Viradouro', study=study
        )
        self.assertIn(collaborator, study.collaborators.all())

    def test_cannot_save_empty_attributes(self):
        study = Study.objects.first()
        collaborator = Collaborator.objects.create(
            name='', team='', study=study
        )
        with self.assertRaises(ValidationError):
            collaborator.save()
            collaborator.full_clean()


@apply_setup(global_setup_ut)
class RejectJustificationModel(TestCase):

    def setUp(self):
        global_setup_ut()

    def test_default_attributes(self):
        justification = RejectJustification()
        self.assertEqual(justification.message, '')

    def test_cannot_save_empty_attributes(self):
        experiment = Experiment.objects.filter(
            status=Experiment.UNDER_ANALYSIS).first()
        justification = RejectJustification.objects.create(
            message='', experiment=experiment
        )
        with self.assertRaises(ValidationError):
            justification.save()
            justification.full_clean()

    def test_justification_message_is_related_to_one_experiment(self):
        experiment = Experiment.objects.filter(
            status=Experiment.UNDER_ANALYSIS).first()
        justification = RejectJustification(
            message='A justification', experiment=experiment
        )
        justification.save()
        self.assertEqual(justification, experiment.justification)
