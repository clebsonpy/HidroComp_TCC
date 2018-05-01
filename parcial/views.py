from django.views.generic import CreateView, TemplateView, DetailView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import ParcialForm


class ParcialFormView(View):

    form_class = ParcialForm
    template_name = 'parcial/parcial.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})


parcial = ParcialFormView.as_view()
