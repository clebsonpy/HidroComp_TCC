from django.urls import reverse_lazy
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import ParcialForm


class ParcialFormView(FormView):

    form_class = ParcialForm
    template_name = 'parcial/parcial.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})


parcial = ParcialFormView.as_view()
