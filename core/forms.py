from django import forms

from odm2admin.models import Results


class ResultsForm(forms.ModelForm):

    class Meta:
        model = Results
        fields = '__all__'