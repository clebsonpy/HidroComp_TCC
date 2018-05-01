from django import forms


class ParcialForm(forms.Form):

    station = forms.CharField(label='Estação', max_length=25)
    font = forms.CharField(label='Fonte', max_length=25)
    date_start = forms.DateField(label='Data Início', required=False)
    date_end = forms.DateField(label='Data Fim', required=False)
    type_threshold = forms.CharField(label='Tipo Limiar', max_length=25)
    value_threshold = forms.FloatField(label='Valor Limiar')
    type_criterion = forms.CharField(label='Critério', max_length='50')
    type_event = forms.CharField(label='Evento', max_length=25)
    duration = forms.IntegerField(label='Duração entre eventos', required=False)
