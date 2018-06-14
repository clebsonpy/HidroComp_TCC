from django import forms

from odm2admin.models import Results


class ParcialForm(forms.Form):
    type_threshold_choices = (
        ('1', 'stationary'),
        ('2', 'events_by_year'))

    type_criterion_choices = (
        ('1', 'mediana'),
        ('2', 'xmin_maior_qmin'),
        ('3', 'xmin_maior_dois_terco_x'),
        ('4', 'autocorrelação'))

    type_event_choices = (
        ('1', 'cheia'),
        ('2', 'estiagem'),)

    station = forms.ModelChoiceField(label='Station', queryset=Results.objects.all())
    source = forms.CharField(label='Source', max_length=25)
    date_start = forms.DateField(label='Start Date', required=False)
    date_end = forms.DateField(label='End Date', required=False)
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


class MaximasForm(forms.Form):

    station = forms.ModelChoiceField(label='Station', queryset=Results.objects.all())
    source = forms.CharField(label='Source', max_length=25)
    date_start = forms.DateField(label='Start Date', required=False)
    date_end = forms.DateField(label='End Date', required=False)

    def __init__(self, *args, **kwargs):
        super(MaximasForm, self).__init__(*args, **kwargs)


class SeriesResultsForm(forms.Form):

    return_period = forms.FloatField(label='Return Period', required=True)

    def __init__(self, *args, **kwargs):
        super(SeriesResultsForm, self).__init__(*args, **kwargs)