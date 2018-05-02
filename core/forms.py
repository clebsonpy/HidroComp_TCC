from django import forms

from ajax_select import make_ajax_field

from odm2admin.models import (Results, Units, Variables, Processinglevels,
                              Samplingfeatures, Actions, Methods, Featureactions)

from odm2admin.forms import (UnitsAdminForm, ResultsAdminForm, VariablesAdminForm,
                             ProcessingLevelsAdminForm, FeatureactionsAdminForm,
                             ActionsAdminForm, MethodsAdminForm,
                             TimeseriesresultvaluesAdminForm)

from betterforms.multiform import MultiModelForm


class SamplingFeaturesForm(forms.ModelForm):

    sampling_feature_type = make_ajax_field(Samplingfeatures, 'sampling_feature_type',
                                            'cv_sampling_feature_type')

    class Meta:
        model = Samplingfeatures
        fields = '__all__'


class ResultsForm(ResultsAdminForm):

    class Meta:
        model = Results
        exclude = ['taxonomicclassifierid', 'resultdatetime', 'validdatetime',
                   'resultdatetimeutcoffset', 'validdatetimeutcoffset']


class FeatureForm(forms.ModelForm):

    class Meta:
        model = Featureactions
        fields = '__all__'


class ResultsMultiForm(MultiModelForm):

    form_classes = {'results': ResultsForm}

    def save(self, commit=True):
        objects = super(ResultsMultiForm, self).save(commit=False)

        if commit:
            processing = objects['processing']
            processing.save()
            results = objects['results']
            results.processing = processing
            results.save()

        return objects


class TimeSeriesResultsForm(TimeseriesresultvaluesAdminForm):

    pass