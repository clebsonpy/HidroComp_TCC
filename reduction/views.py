from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView

import pandas as pd
import plotly.offline as opy
from HydroComp.series.flow import Flow

from .forms import ParcialForm, MaximasForm, SeriesResultsForm
from odm2admin.models import Timeseriesresultvalues, Timeseriesresults


def get_data(post):
    time_series = Timeseriesresultvalues.objects.filter(
        resultid=post['station']).values_list('datavalue', 'valuedatetime')

    results_obj = Timeseriesresults.objects.get(pk=post['station'])
    station = results_obj.resultid.featureactionid.samplingfeatureid.samplingfeaturename

    dic = {'Data': [], station: []}
    for i in time_series:
        dic['Data'].append(i[1])
        dic[station].append(i[0])
    data = pd.DataFrame(dic, index=dic['Data'], columns=[station])
    return data.sort_index(), station


class ParcialFormView(FormView):

    form_class = ParcialForm
    template_name = 'reduction/series_partial.html'
    success_url = reverse_lazy('series:results')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        post = request.POST

        data, station = get_data(post)
        type_criterion = self.form_class.type_criterion_choices[int(post['type_criterion'])-1][1]
        type_threshold = self.form_class.type_threshold_choices[int(post['type_threshold'])-1][1]
        type_event = self.form_class.type_event_choices[int(post['type_event'])-1][1]

        series = Flow(data=data, source=station)
        if post['date_start'] != '':
            series.date(date_start=post['date_start'], date_end=post['date_end'])

        parcial = series.parcial(station=station,
                                type_threshold=type_threshold,
                                type_event=type_event,
                                type_criterion=type_criterion,
                                value_threshold=float(post['value_threshold']),
                                duration=float(post['duration']))

        fig, data = parcial.plot_hydrogram('Parcial')

        div = opy.plot(fig, auto_open=False, output_type='div')

        context = {#'return_magn': return_magn,
                   #'return_time': post['return_time'],
                   'graphs': div
                   }
        return render(request, 'reduction/serie_result.html', context=context)


class MaximaFormView(FormView):

    form_class = MaximasForm
    template_name = 'reduction/series_maximum.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.request.POST

        data, station = get_data(post)
        series = Flow(data=data, source=station)

        if post['date_start'] != '':
            series.date(date_start=post['date_start'], date_end=post['date_end'])

        maxima = series.maximum(station)

        self.request.COOKIES['serie'] = maxima

        data, fig = maxima.plot_hydrogram()
        div = opy.plot(data, auto_open=False, output_type='div')
        magn = dict()
        for i in [2, 10, 20, 30, 50, 100]:
            magn[i] = round(maxima.magnitude(i, estimador='mml'), 3)

        context = {'magn': magn, 'graphs': div}
        return render(request, 'reduction/serie_result.html', context=context)


class SerieRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        post = self.request.POST

        data, station = get_data(post)
        series = Flow(data=data, source=station)

        if post['date_start'] != '':
            series.date(date_start=post['date_start'], date_end=post['date_end'])

        maxima = series.maximum(station)

        self.request.COOKIES['serie'] = maxima

        data, fig = maxima.plot_hydrogram()
        div = opy.plot(data, auto_open=False, output_type='div')
        self.request.COOKIES['div'] = div

        return reverse('reduction:results')


class SeriesResultsView(TemplateView):

    template_name = 'reduction/serie_result.html'

    def get_context_data(self, **kwargs):
        context = super(SeriesResultsView, self).get_context_data(**kwargs)
        context['form'] = SeriesResultsForm
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


parcial = ParcialFormView.as_view()
maximum = MaximaFormView.as_view()
redirect = RedirectView.as_view()
results = SeriesResultsView.as_view()
