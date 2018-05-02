from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from odm2admin.models import (Results, Units, Variables, Featureactions,
                              Timeseriesresultvalues)

from odm2admin.forms import (VariablesAdminForm, UnitsAdminForm,
                             TimeseriesresultvaluesAdminForm)

from .forms import (ResultsMultiForm, FeatureActionsMultiForm)


class IndexView(TemplateView):

    template_name = 'index.html'


class ResultsIndexView(TemplateView):

    template_name = 'results_index.html'


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


class FeatureActionsView(CreateView):

    model = Featureactions
    template_name = 'feature_actions.html'
    form_class = FeatureActionsMultiForm
    success_url = reverse_lazy('dados:index')


class TimeSerieResultsView(CreateView):

    model = Timeseriesresultvalues
    form_class = TimeseriesresultvaluesAdminForm
    template_name = 'time_series.html'
    success_url = reverse_lazy('dados:index')


index = IndexView.as_view()
results_index = ResultsIndexView.as_view()
feature = FeatureActionsView.as_view()
results = ResultsFormView.as_view()
variables = VariablesView.as_view()
units = UnitsView.as_view()
time_series = TimeSerieResultsView.as_view()