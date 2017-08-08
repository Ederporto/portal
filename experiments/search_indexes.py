from haystack import indexes

from experiments.models import Experiment, Study, Group, ExperimentalProtocol


class ExperimentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    owner = indexes.CharField(model_attr='owner')

    def get_model(self):
        return Experiment

    def index_queryset(self, using=None):
        return self.get_model().lastversion_objects.filter(
            status=Experiment.APPROVED
        )


class StudyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    experiment = indexes.CharField(model_attr='experiment__id')
    keywords = indexes.CharField(model_attr='keywords__name')
    researcher = indexes.CharField(model_attr='researcher__id')
    collaborators = indexes.CharField(model_attr='collaborators__name')

    def get_model(self):
        return Study

    def index_queryset(self, using=None):
        experiments = Experiment.lastversion_objects.filter(
            status=Experiment.APPROVED
        )
        return self.get_model().objects.filter(experiment__in=experiments)


class GroupIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    experiment = indexes.CharField(model_attr='experiment__id')
    inclusion_criteria = indexes.CharField(model_attr='inclusion_criteria__id')

    def get_model(self):
        return Group

    def index_queryset(self, using=None):
        experiments = Experiment.lastversion_objects.filter(
            status=Experiment.APPROVED
        )
        return self.get_model().objects.filter(experiment__in=experiments)


class ExperimentalProtocolIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    group = indexes.CharField(model_attr='group__id')

    def get_model(self):
        return ExperimentalProtocol

    def index_queryset(self, using=None):
        experiments = Experiment.lastversion_objects.filter(
            status=Experiment.APPROVED
        )
        groups = Group.objects.filter(experiment__in=experiments)
        return self.get_model().objects.filter(group__in=groups)
