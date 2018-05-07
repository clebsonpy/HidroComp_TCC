from django import forms
from collections import OrderedDict

from ajax_select import make_ajax_field

from odm2admin.models import (Results, Samplingfeatures, Featureactions,
                              Timeseriesresults, Timeseriesresultvalues, Organizations)

from odm2admin.forms import (ResultsAdminForm, TimeseriesresultvaluesAdminForm,
                             TimeseriesresultsAdminForm, OrganizationsAdminForm)

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


class TimeSeriesResultsForm(TimeseriesresultsAdminForm):

    def __init__(self, *args, **kwargs):
        super(TimeSeriesResultsForm, self).__init__(*args, **kwargs)
        self.fields['aggregationstatisticcv'].label = 'Aggregation Statistic'

    class Meta:
        model = Timeseriesresults
        fields = ['aggregationstatisticcv', 'intendedtimespacing',
                  'resultid', 'intendedtimespacingunitsid',
                  'spatialreferenceid']


class TimeResultsSeriesValuesForm(TimeseriesresultvaluesAdminForm, forms.Form):

    def __init__(self, *args, **kwargs):
        super(TimeResultsSeriesValuesForm, self).__init__(*args, **kwargs)
        self.fields['valuedatetimeutcoffset'].label = 'Value UTC'
        self.fields['censorcodecv'].label = 'Censor Code'
        self.fields['qualitycodecv'].label = 'Quality Code'
        self.fields['File'] = forms.FileField()

    class Meta:
        model = Timeseriesresultvalues
        exclude = ['datavalue', 'valuedatetime']
        ordering = ['valuedatetimeutcoffset', 'censorcodecv',
                    'qualitycodecv', 'File']


class TimeResultsSeriesValuesMultiForm(MultiModelForm):

    form_classes = OrderedDict((
        ('time_results', TimeSeriesResultsForm),
        ('time_series_results', TimeResultsSeriesValuesForm)))


class OrganizationsForm(OrganizationsAdminForm):

    class Meta:
        model = Organizations
        fields = ['organizationcode', 'organizationname',
                  'organizationtypecv', 'parentorganizationid']