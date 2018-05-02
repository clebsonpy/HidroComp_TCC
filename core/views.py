from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from odm2admin.models import (Results, Units, Variables, Featureactions,
                              Timeseriesresultvalues, Samplingfeatures, Actions,
                              Methods, Processinglevels)

from odm2admin.forms import (VariablesAdminForm, UnitsAdminForm, ActionsAdminForm,
                             TimeseriesresultvaluesAdminForm, FeatureactionsAdminForm,
                             MethodsAdminForm, ProcessingLevelsAdminForm)

from .forms import (ResultsMultiForm, SamplingFeaturesForm, FeatureForm)


class IndexView(TemplateView):

    template_name = 'index.html'


class ResultsIndexView(TemplateView):

    template_name = 'data_index.html'


class ResultsFormView(CreateView):

    model = Results
    template_name = 'results.html'
    form_class = ResultsMultiForm
    success_url = reverse_lazy('index')


class VariablesView(CreateView):

    model = Variables
    template_name = 'variables.html'
    form_class = VariablesAdminForm
    success_url = reverse_lazy('index')


class UnitsView(CreateView):

    model = Units
    template_name = 'units.html'
    form_class = UnitsAdminForm
    success_url = reverse_lazy('index')


class ActionsView(CreateView):

    model = Actions
    template_name = 'actions.html'
    form_class = ActionsAdminForm
    success_url = reverse_lazy('dados:index')


class TimeSerieResultsView(CreateView):

    model = Timeseriesresultvalues
    form_class = TimeseriesresultvaluesAdminForm
    template_name = 'time_series.html'
    success_url = reverse_lazy('dados:index')


class SamplingFeatureView(CreateView):

    model = Samplingfeatures
    form_class = SamplingFeaturesForm
    template_name = 'sampling_feature.html'
    success_url = reverse_lazy('dados:index')


class MethodsView(CreateView):

    model = Methods
    form_class = MethodsAdminForm
    template_name = 'methods.html'
    success_url = reverse_lazy('dados:index')


class ProcessingLevesView(CreateView):

    model = Processinglevels
    form_class = ProcessingLevelsAdminForm
    template_name = 'processing_leves.html'
    success_url = reverse_lazy('dados:index')


class FeatureActionsView(CreateView):

    model = Featureactions
    form_class = FeatureForm
    template_name = 'feature.html'
    success_url = reverse_lazy('dados:index')


index = IndexView.as_view()
results_index = ResultsIndexView.as_view()
actions = ActionsView.as_view()
sampling_feature = SamplingFeatureView.as_view()
feature = FeatureActionsView.as_view()
methods = MethodsView.as_view()
processing_level = ProcessingLevesView.as_view()
results = ResultsFormView.as_view()
variables = VariablesView.as_view()
units = UnitsView.as_view()
time_series = TimeSerieResultsView.as_view()