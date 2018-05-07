from django.views.generic import CreateView, TemplateView, DetailView, FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import ParcialForm


class ParcialFormView(FormView):

    form_class = ParcialForm
    template_name = 'parcial/parcial.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form['station'].value())
        if form.is_valid():
            return HttpResponseRedirect('index')

        return render(request, self.template_name, {'form': form})


parcial = ParcialFormView.as_view()
