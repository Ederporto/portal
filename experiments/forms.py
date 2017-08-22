from django import forms
from django.utils.translation import ugettext as _
from haystack.forms import SearchForm


class NepSearchForm(SearchForm):
    q = forms.CharField(
        required=True, label='',
        widget=forms.TextInput(
            attrs={'type': 'search',
                   'placeholder': 'Type key terms/words to be searched',
                   'class': 'search-box'}
        )
    )

    filter = forms.MultipleChoiceField(
        required=False, label='',
        choices=[
            ('eeg', _('EEG')), ('tms', _('TMS')), ('emg', _('EMG')),
            ('goalkeeper', _('Goalkeeper game phase')),
            ('cinematic', _('Kinematic measures')),
            ('stabilometry', _('Stabilometry')),
            ('answertime', _('Response time')),
            ('psychophysical', _('Psychophysical measures')),
            ('verbal', _('Verbal response')),
            ('psychometric', _('Psychometric scales')),
            ('unitary', _('Unit recording')),
            ('multiunit', _('Multiunit recording'))
        ],
        widget=forms.SelectMultiple(
            attrs={'id': 'filter_box', 'class': 'selectpicker search-select'}
        )
    )

    def search(self):
        sqs = super(NepSearchForm, self).search()
        sqs = self._parse_query(self.cleaned_data['q'], sqs)

        return sqs

    def _parse_query(self, query, sqs):
        """
        Parse query treating modifiers 'AND', 'OR', 'NOT' to make what they're
        supposed to.
        :param query: query entered in search input box in form
        :param sqs: SearchQuerySet until now
        :return: SearchQuerySet object
        """
        words = iter(query.split())
        result = sqs

        for word in words:
            try:
                if word == 'AND':
                    result = result.filter_and(content=words.__next__())
                # elif word == 'OR':
                #     result = result.filter_or(content=words.__next__())
                # elif word == 'NOT':
                #     result = result.exclude(content=words.__next__())
                else:
                    result = result.filter(content=word)
            except StopIteration:
                return result

        return result
