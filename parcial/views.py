from django.views.generic import CreateView, TemplateView, DetailView
from django.shortcuts import render


class ParcialView(TemplateView):

    template_name = 'parcial/parcial.html'

parcial = ParcialView.as_view()