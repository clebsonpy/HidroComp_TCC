from django import forms

from odm2admin.models import Results, Units, Variables, Processinglevels
from odm2admin.forms import (UnitsAdminForm, ResultsAdminForm, VariablesAdminForm,
                             ProcessingLevelsAdminForm)

from betterforms.multiform import MultiModelForm


class ResultsForm(ResultsAdminForm):

    class Meta:
        model = Results
        exclude = ['unitsid', 'variableid', 'featureactionid', 'taxonomicclassifierid',
                   'statuscv', 'processing_level']

class VariablesForm(VariablesAdminForm):

    class Meta:
        model = Variables
        exclude = ['variabledefinition']


class UnitsForm(UnitsAdminForm):

    class Meta:
        model = Units
        exclude = ['unitslink']


class ProcessinglevelsForm(ProcessingLevelsAdminForm):

    class Meta:
        model = Processinglevels
        fields = ['processinglevelcode']


class ResultsMultiForm(MultiModelForm):

    form_classes = {'results': ResultsForm, 'units': UnitsForm,
                    'variables': VariablesForm, 'processing': ProcessinglevelsForm}

    def save(self, commit=True):
        objects = super(ResultsMultiForm, self).save(commit=False)

        if commit:
            processing = objects['processing']
            processing.save()
            units = objects['units']
            units.save()
            variables = objects['variables']
            variables.save()
            results = objects['results']
            results.processing = processing
            results.units = units
            results.variables = variables
            results.save()

        return objects
