import pandas as pd
import numpy as np
import plotly.plotly as py
import scipy.stats as stat
from lmoments3 import distr

from HidroComp.graphics.genextreme import GenExtreme
from HidroComp.graphics.hydrogram_annual import HydrogramAnnual


class Maximum(object):

    distribution = 'GEV'

    def __init__(self, obj, station):
        self.obj = obj
        self.data = self.obj.data
        self.station = station

    def annual(self):
        data_by_year_hydrologic = self.data.groupby(pd.Grouper(
            freq='AS-%s' % self.obj.month_start_year_hydrologic(self.station)[1]))
        max_vazao = data_by_year_hydrologic[self.station].max().values
        idx_vazao = data_by_year_hydrologic[self.station].idxmax().values

        self.peaks = pd.DataFrame(max_vazao, index=idx_vazao, columns=['Vazao'])
        return self.peaks

    def mml(self):
        try:
            peaks = self.peaks.copy()
            mom = distr.gev.lmom_fit(peaks['Vazao'].values)
            self.para = [mom['c'], mom['loc'], mom['scale']]
            return self.para
        except AttributeError:
            self.annual()
            return self.mml()

    def mvs(self):
        try:
            peaks = self.peaks.copy()
            self.para = stat.genextreme.fit(peaks['Vazao'].values)
            return self.para
        except AttributeError:
            self.annual()
            return self.mvs()

    def magnitude(self, period_return):

        try:
            prob = 1-(1/period_return)
            mag = stat.genpareto.ppf(prob, self.para[0], self.para[1],
                                     self.para[2])
            return mag

        except AttributeError:
            self.mml()
            return self.magnitude(period_return)

    def plot_distribution(self, title, estimador, type_function):
        if estimador == 'mvs':
            para = self.mvs()
        elif estimador == 'mml':
            para = self.mml()
        else:
            raise ValueError
        genextreme = GenExtreme(title, para[0], para[1], para[2])
        data, fig = genextreme.plot(type_function)
        return data, fig

    def plot_hydrogram(self):
        self.annual()
        hydrogrm = HydrogramAnnual(data=self.data[self.station],
                                   peaks=self.peaks)
        data, fig = hydrogrm.plot()
        #py.image.save_as(fig, filename='gráficos/hidrogama_maximas_anuais.png')

        return data, fig
