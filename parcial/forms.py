from django import forms


class ParcialForm(forms.Form):

    station = forms.CharField(label='Station', max_length=25)
    font = forms.CharField(label='Font', max_length=25)
    date_start = forms.DateField(label='Start Date', required=False)
    date_end = forms.DateField(label='End Start', required=False)
    type_threshold = forms.CharField(label='Threshold type', max_length=25)
    value_threshold = forms.FloatField(label='Threshold Value')
    type_criterion = forms.CharField(label='Criterion', max_length='50')
    type_event = forms.CharField(label='Event', max_length=25)
    duration = forms.IntegerField(label='Duration Eetween Events', required=False)

    def __init__(self, *args, **kwargs):
        super(ParcialForm, self).__init__(*args, **kwargs)
