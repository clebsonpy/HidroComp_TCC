import os
import pandas as pd

from abc import abstractmethod, ABCMeta

from HidroComp.files import *


class Series(object, metaclass=ABCMeta):

    fonts = {
        "ONS": ons.Ons,
        "ANA": ana.Ana
    }

    def __init__(self, data=None, path=os.getcwd(), font=None, *args, **kwargs):
        self.path = path
        if data is not None:
            self.data = data
        else:
            if font in self.fonts:
                self.data = self.fonts[font](self.path, *args, **kwargs).data
            else:
                raise KeyError('Font not supported!')

        self.date_start = self.data.index[0]
        self.date_end = self.data.index[-1]

    @abstractmethod
    def month_start_year_hydrologic(self, station):
        pass

    @abstractmethod
    def plot_hydrogram(self):
        pass

    def date(self, date_start=None, date_end=None):
        if date_start is not None and date_end is not None:
            self.date_start = pd.to_datetime(date_start, dayfirst=True)
            self.date_end = pd.to_datetime(date_end, dayfirst=True)
            self.data = self.data.loc[self.date_start:self.date_end]
        elif date_start is not None:
            self.date_start = pd.to_datetime(date_start, dayfirst=True)
            self.data = self.data.loc[self.date_start:]
        elif date_end is not None:
            self.date_end = pd.to_datetime(date_end, dayfirst=True)
            self.data = self.data.loc[:self.date_end]

    def flawless_period(self, station):
        aux = []
        list_start = []
        list_end = []
        gantt_bool = self.data.isnull()[station]
        for i in gantt_bool.index:
            if ~gantt_bool.loc[i]:
                aux.append(i)
            elif len(aux) > 2 and gantt_bool.loc[i]:
                list_start.append(aux[0])
                list_end.append(aux[-1])
                aux = []
        if len(aux) > 0:
            list_start.append(aux[0])
            list_end.append(aux[-1])
        dic = {'Inicio': list_start, 'Fim': list_end}
        return pd.DataFrame(dic)