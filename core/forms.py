from django import forms

from ajax_select import make_ajax_field

from odm2admin.models import (Results, Units, Variables, Processinglevels,
                              Samplingfeatures, Actions, Methods, Featureactions)

from odm2admin.forms import (UnitsAdminForm, ResultsAdminForm, VariablesAdminForm,
                             ProcessingLevelsAdminForm, FeatureactionsAdminForm,
                             ActionsAdminForm, MethodsAdminForm)

from betterforms.multiform import MultiModelForm


class SamplingFeaturesForm(forms.ModelForm):

    sampling_feature_type = make_ajax_field(Samplingfeatures, 'sampling_feature_type',
                                            'cv_sampling_feature_type')

    class Meta:
        model = Samplingfeatures
        fields = ['sampling_feature_type', 'samplingfeaturecode']


class ActionsForm(ActionsAdminForm):

    class Meta:
        model = Actions
        exclude = ['actiondescription', 'enddatetime', 'enddatetimeutcoffset',
                   'method', 'actionfilelink']


class MethodsForm(MethodsAdminForm):

    class Meta:
        model = Methods
        fields = ['methodtypecv', 'methodname', 'methodcode']


class FeatureActionsForm(FeatureactionsAdminForm):

    class Meta:
        model = Featureactions
        exclude = ['action', 'samplingfeatureid']


class FeatureActionsMultiForm(MultiModelForm):

    form_classes = {'actions': ActionsForm, 'methods': MethodsForm,
                    'sampling_feature': SamplingFeaturesForm,
                    'feature_actions': FeatureActionsForm}


    def save(self, commit=True):
        objects = super(FeatureActionsMultiForm, self).save(commit=False)

        if commit:
            sampling_feature = objects['sampling_feature']
            sampling_feature.save()
            methods = objects['methods']
            methods.save()
            actions = objects['actions']
            actions.methods = methods
            actions.save()
            feature_actions = objects['feature_actions']
            feature_actions.sampling_feature = sampling_feature
            feature_actions.actions = actions
            feature_actions.save()

        return objects


class VariablesForm(VariablesAdminForm):

    class Meta:
        model = Variables
        exclude = ['variabledefinition']


class UnitsForm(UnitsAdminForm):

    class Meta:
        model = Units
        exclude = ['unitslink']


class ResultsForm(ResultsAdminForm):

    class Meta:
        model = Results
        exclude = ['taxonomicclassifierid', 'resultdatetime', 'validdatetime',
                   'resultdatetimeutcoffset', 'validdatetimeutcoffset']


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
