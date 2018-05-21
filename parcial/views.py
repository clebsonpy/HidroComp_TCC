from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView, CreateView
from django.shortcuts import render, redirect

import pandas as pd
import plotly.offline as opy
from HidroComp.series.vazao import Vazao

from .forms import ParcialForm
from odm2admin.models import Timeseriesresultvalues


class ParcialFormView(FormView):

    form_class = ParcialForm
    template_name = 'parcial/parcial.html'
    success_url = reverse_lazy('parcial:hydrogram')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        post = request.POST
        time_serie = Timeseriesresultvalues.objects.filter(resultid=post['station']).values_list('datavalue', 'valuedatetime')
        dic = {'Data': [], post['font']: []}
        for i in time_serie:
            dic['Data'].append(i[1])
            dic[post['font']].append(i[0])

        type_criterion = self.form_class.type_criterion_choices[int(post['type_criterion'])-1][1]
        type_threshold = self.form_class.type_threshold_choices[int(post['type_threshold'])-1][1]
        type_event = self.form_class.type_event_choices[int(post['type_event'])-1][1]

        data = pd.DataFrame(dic, index=dic['Data'], columns=[post['font']])
        serie = Vazao(data=data, font=post['font'])
        if post['date_start'] != '':
            serie.date(date_start=post['date_start'], date_end=post['date_end'])

        parcial = serie.parcial(station=post['font'],
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
        return render(request, 'parcial/parcial_result.html', context)


parcial = ParcialFormView.as_view()
