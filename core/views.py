from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from odm2admin.models import Results

from .forms import ResultsForm


class IndexView(TemplateView):

    template_name = 'index.html'


class ResultsFormView(CreateView):

    model = Results
    template_name = 'results.html'
    form_class = ResultsForm
    success_url = reverse_lazy('index')


index = IndexView.as_view()
results = ResultsFormView.as_view()