from django import forms

from odm2admin.models import Results, Organizations


class SeriesForm(forms.Form):

    station = forms.ModelChoiceField(label='Station', queryset=Results.objects.all())
    source = forms.ModelChoiceField(
        label='Source', queryset=Organizations.objects.all()
    )
    date_start = forms.DateField(label='Start Date', required=False)
    date_end = forms.DateField(label='End Date', required=False)

    def __init__(self, *args, **kwargs):
        super(SeriesForm, self).__init__(*args, **kwargs)


class SeriesResultsForm(forms.Form):

    return_period = forms.FloatField(label='Return Period', required=True)

    def __init__(self, *args, **kwargs):
        super(SeriesResultsForm, self).__init__(*args, **kwargs)


class ParcialForm(SeriesForm):
    type_threshold_choices = (
        ('1', 'stationary'),
        ('2', 'events_by_year'))

    type_criterion_choices = (
        ('1', 'median'),
        ('2', 'xmin_larger_qmin'),
        ('3', 'xmin_larger_dois_terco_x'),
        ('4', 'autocorrelation'))

    type_event_choices = (
        ('1', 'flood'),
        ('2', 'drought'),)

    type_threshold = forms.ChoiceField(label='Threshold type',
                                       choices=type_threshold_choices, )
    value_threshold = forms.FloatField(label='Threshold Value')
    type_criterion = forms.ChoiceField(label='Criterion',
                                       choices=type_criterion_choices)
    type_event = forms.ChoiceField(label='Event',
                                   choices=type_event_choices)
    duration = forms.IntegerField(label='Duration Between Events', required=False)

    def __init__(self, *args, **kwargs):
        super(ParcialForm, self).__init__(*args, **kwargs)


class MaximasForm(SeriesForm):

    def __init__(self, *args, **kwargs):
        super(MaximasForm, self).__init__(*args, **kwargs)
