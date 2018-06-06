from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.shortcuts import render, redirect, render_to_response
from django.template import loader

import pandas as pd
import plotly.offline as opy
from HidroComp.series.vazao import Vazao

from .forms import ParcialForm, MaximasForm, SeriesResultsForm
from odm2admin.models import Timeseriesresultvalues


class ParcialFormView(FormView):

    form_class = ParcialForm
    template_name = 'parcial/parcial.html'
    success_url = reverse_lazy('series:results')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        post = request.POST
        time_serie = Timeseriesresultvalues.objects.filter(
            resultid=post['station']).values_list('datavalue', 'valuedatetime')
        dic = {'Data': [], post['source']: []}
        for i in time_serie:
            dic['Data'].append(i[1])
            dic[post['source']].append(i[0])

        type_criterion = self.form_class.type_criterion_choices[int(post['type_criterion'])-1][1]
        type_threshold = self.form_class.type_threshold_choices[int(post['type_threshold'])-1][1]
        type_event = self.form_class.type_event_choices[int(post['type_event'])-1][1]

        data = pd.DataFrame(dic, index=dic['Data'], columns=[post['source']])
        serie = Vazao(data=data, source=post['source'])
        if post['date_start'] != '':
            serie.date(date_start=post['date_start'], date_end=post['date_end'])

        parcial = serie.parcial(station=post['source'],
                                type_threshold=type_threshold,
                                type_event=type_event,
                                type_criterion=type_criterion,
                                value_threshold=float(post['value_threshold']),
                                duration=float(post['duration']))

        return_magn = parcial.magnitude(float(post['return_time']))

        fig = parcial.plot_hydrogram('Parcial')
        div = opy.plot(fig, auto_open=False, output_type='div')
        context = {'return_magn': return_magn,
                   'return_time': post['return_time'],
                   'graphs': div
                   }
        return HttpResponse(render(request, context))


class MaximaFormView(FormView):

    form_class = MaximasForm
    template_name = 'parcial/maximas.html'
    success_url = reverse_lazy('series:results')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        post = request.POST
        time_serie = Timeseriesresultvalues.objects.filter(
            resultid=post['station']).values_list('datavalue', 'valuedatetime')
        dic = {'Data': [], post['source']: []}
        for i in time_serie:
            dic['Data'].append(i[1])
            dic[post['source']].append(i[0])

        data = pd.DataFrame(dic, index=dic['Data'], columns=[post['source']])
        serie = Vazao(data=data, source=post['source'])
        if post['date_start'] != '':
            serie.date(date_start=post['date_start'], date_end=post['date_end'])

        maxima = serie.maximum(post['source'])

        request.COOKIES['serie'] = maxima
        #return_magn = maxima.magnitude(float(post['return_time']))

        data, fig = maxima.plot_hydrogram()
        div = opy.plot(data, auto_open=False, output_type='div')
        context = {'graphs': div,
                   'form': SeriesResultsForm}
        return render(request, 'parcial/serie_result.html', context=context)


class SeriesResultsView(FormView):

    form_class = SeriesResultsForm
    template_name = 'parcial/serie_result.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        pass

parcial = ParcialFormView.as_view()
maximas = MaximaFormView.as_view()
results = SeriesResultsView.as_view()
