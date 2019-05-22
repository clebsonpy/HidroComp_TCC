from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.core.files.uploadedfile import UploadedFile

import pandas as pd

from odm2admin.models import (Results, Units, Variables, Featureactions,
                              Timeseriesresultvalues, Samplingfeatures, Actions,
                              Methods, Processinglevels, Organizations, Timeseriesresults, CvCensorcode, CvQualitycode)

from odm2admin.forms import (VariablesAdminForm, UnitsAdminForm, ActionsAdminForm,
                             MethodsAdminForm, ProcessingLevelsAdminForm)
from pytz import NonExistentTimeError, AmbiguousTimeError

from core.forms import ResultsForm
from .forms import (SamplingFeaturesForm, FeatureForm, OrganizationsForm,
                    TimeResultsSeriesValuesForm, TimeSeriesResultsForm)


class IndexView(TemplateView):

    template_name = 'index.html'


class ResultsIndexView(TemplateView):

    template_name = 'data_index.html'


class ResultsView(CreateView):

    model = Results
    template_name = 'results.html'
    form_class = ResultsForm
    success_url = reverse_lazy('dados:time_serie_result')


class VariablesView(CreateView):

    model = Variables
    template_name = 'variables.html'
    form_class = VariablesAdminForm
    success_url = reverse_lazy('dados:units')


class UnitsView(CreateView):

    model = Units
    template_name = 'units.html'
    form_class = UnitsAdminForm
    success_url = reverse_lazy('dados:processinglevel')


class ActionsView(CreateView):

    model = Actions
    template_name = 'actions.html'
    form_class = ActionsAdminForm
    success_url = reverse_lazy('dados:feature')


class TimeSerieResultsValuesView(CreateView):

    model = Timeseriesresultvalues
    form_class = TimeResultsSeriesValuesForm
    template_name = 'time_series.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        file = request.FILES['File']
        dados = pd.read_csv(file, index_col=0, names=["Data", "XINGO"],
                            parse_dates=True)
        print(len(dados))
        post = request.POST
        result = Timeseriesresults.objects.get(pk=post['resultid'])
        censor = CvCensorcode.objects.get(pk=post['censorcodecv'])
        quality = CvQualitycode.objects.get(pk=post['qualitycodecv'])
        units_time = Units.objects.get(pk=post['timeaggregationintervalunitsid'])
        time_inter = post['timeaggregationinterval']
        value_utc = post['valuedatetimeutcoffset']

        nAdd = []
        for i in dados.index:
            print(i)
            try:
                ts = Timeseriesresultvalues(resultid=result, censorcodecv=censor,
                                            qualitycodecv=quality, valuedatetimeutcoffset=value_utc,
                                            timeaggregationinterval=time_inter,
                                            timeaggregationintervalunitsid=units_time,
                                            valuedatetime=i,
                                            datavalue=dados[1][i])

                ts.save()
            except (NonExistentTimeError, AmbiguousTimeError):
                nAdd.append(ts)

        return redirect(self.success_url)


class SamplingFeatureView(CreateView):

    model = Samplingfeatures
    form_class = SamplingFeaturesForm
    template_name = 'sampling_feature.html'
    success_url = reverse_lazy('dados:methods')


class MethodsView(CreateView):

    model = Methods
    form_class = MethodsAdminForm
    template_name = 'methods.html'
    success_url = reverse_lazy('dados:actions')


class ProcessingLevesView(CreateView):

    model = Processinglevels
    form_class = ProcessingLevelsAdminForm
    template_name = 'processing_leves.html'
    success_url = reverse_lazy('dados:results')


class FeatureActionsView(CreateView):

    model = Featureactions
    form_class = FeatureForm
    template_name = 'feature.html'
    success_url = reverse_lazy('dados:variables')


class OrganizationsView(CreateView):

    model = Organizations
    form_class = OrganizationsForm
    template_name = 'organizations.html'
    success_url = reverse_lazy('dados:samplingfeature')


class TimeSeriesResultsView(CreateView):

    model = Timeseriesresults
    form_class = TimeSeriesResultsForm
    template_name = 'time_series_results.html'
    success_url = reverse_lazy('index')


index = IndexView.as_view()
results_index = ResultsIndexView.as_view()
actions = ActionsView.as_view()
sampling_feature = SamplingFeatureView.as_view()
feature = FeatureActionsView.as_view()
methods = MethodsView.as_view()
processing_level = ProcessingLevesView.as_view()
results = ResultsView.as_view()
variables = VariablesView.as_view()
units = UnitsView.as_view()
organizations = OrganizationsView.as_view()
time_series = TimeSerieResultsValuesView.as_view()
time_serie_result = TimeSeriesResultsView.as_view()
