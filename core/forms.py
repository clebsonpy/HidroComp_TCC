from django import forms

from odm2admin.models import Results, Units, Variables
from odm2admin.forms import (UnitsAdminForm, ResultsAdminForm, VariablesAdminForm)

from betterforms.multiform import MultiModelForm


class ResultsForm(ResultsAdminForm):

    class Meta:
        model = Results
        exclude = ['unitsid', 'variableid']

class VariablesForm(VariablesAdminForm):

    class Meta:
        model = Variables
        exclude = ['variabledefinition']


class UnitsForm(UnitsAdminForm):

    class Meta:
        model = Units
        exclude = ['unitslink']


class ResultsMultiForm(MultiModelForm):

    form_classes = {'results': ResultsForm,
                    'units': UnitsForm,
                    'variables': VariablesForm}

    def save(self, commit=True):
        objects = super(ResultsMultiForm, self).save(commit=False)

        if commit:
            units = objects['units']
            units.save()
            variables = objects['variables']
            variables.save()
            results = objects['results']
            results.units = units
            results.variables = variables
            results.save()

        return objects