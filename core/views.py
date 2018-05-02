from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from odm2admin.models import (Results, Units, Variables, Samplingfeatures,
                              Actions, Methods, Featureactions)

from odm2admin.forms import (ResultsAdminForm, VariablesAdminForm, UnitsAdminForm,
                             TimeseriesresultsAdminForm, TimeseriesresultvaluesAdminForm,
                             RelatedresultsAdminForm)

from .forms import (ResultsMultiForm, UnitsForm, VariablesForm, SamplingFeaturesForm,
                    ActionsForm, MethodsForm, FeatureActionsForm, FeatureActionsMultiForm,
                    ResultsForm)


class IndexView(TemplateView):

    template_name = 'index.html'


class ResultsIndexView(TemplateView):

    template_name = 'results_index.html'


class ResultsFormView(CreateView):

    model = Results
    template_name = 'results.html'
    form_class = ResultsForm
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


index = IndexView.as_view()
results_index = ResultsIndexView.as_view()
feature = FeatureActionsView.as_view()
results = ResultsFormView.as_view()
variables = VariablesView.as_view()
units = UnitsView.as_view()