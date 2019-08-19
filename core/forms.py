from django import forms

from ajax_select import make_ajax_field

from odm2admin.models import (Results, Samplingfeatures, Featureactions,
                              Timeseriesresults, Timeseriesresultvalues, Organizations)

from odm2admin.forms import (ResultsAdminForm, TimeseriesresultvaluesAdminForm,
                             TimeseriesresultsAdminForm, OrganizationsAdminForm)


class SamplingFeaturesForm(forms.ModelForm):

    sampling_feature_type = make_ajax_field(Samplingfeatures, 'sampling_feature_type',
                                            'cv_sampling_feature_type')

    class Meta:
        model = Samplingfeatures
        fields = ['samplingfeaturecode', 'sampling_feature_type', 'samplingfeaturename']


class ResultsForm(ResultsAdminForm):

    class Meta:
        model = Results
        exclude = ['taxonomicclassifierid', 'resultdatetime', 'validdatetime',
                   'resultdatetimeutcoffset', 'validdatetimeutcoffset']


class FeatureForm(forms.ModelForm):

    class Meta:
        model = Featureactions
        fields = '__all__'


class TimeSeriesResultsForm(TimeseriesresultsAdminForm):

    def __init__(self, *args, **kwargs):
        super(TimeSeriesResultsForm, self).__init__(*args, **kwargs)
        self.fields['aggregationstatisticcv'].label = 'Aggregation Statistic'

    class Meta:
        model = Timeseriesresults
        fields = ['aggregationstatisticcv', 'resultid']


class TimeResultsSeriesValuesForm(TimeseriesresultvaluesAdminForm, forms.Form):

    def __init__(self, *args, **kwargs):
        super(TimeResultsSeriesValuesForm, self).__init__(*args, **kwargs)
        self.fields['valuedatetimeutcoffset'].label = 'Value UTC'
        self.fields['censorcodecv'].label = 'Censor Code'
        self.fields['qualitycodecv'].label = 'Quality Code'
        self.fields['File'] = forms.FileField()

    class Meta:
        model = Timeseriesresultvalues
        exclude = ['datavalue', 'valuedatetime', 'resultid']
        ordering = ['valuedatetimeutcoffset', 'censorcodecv',
                    'qualitycodecv', 'File']


class OrganizationsForm(OrganizationsAdminForm):

    class Meta:
        model = Organizations
        fields = ['organizationcode', 'organizationname',
                  'organizationtypecv', 'parentorganizationid']


class GanttForm(forms.Form):
    station = forms.ModelChoiceField(label='Station', queryset=Results.objects.all())
    source = forms.ModelChoiceField(
        label='Source', queryset=Organizations.objects.all()
    )
    def __init__(self, *args, **kwargs):
        super(GanttForm, self).__init__(*args, **kwargs)
