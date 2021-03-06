from unittest import TestCase
import pandas as pd
import os
from HydroComp.iha.iha import IHA


class Test_IHA(TestCase):

    @staticmethod
    def read():
        path = os.path.abspath(os.path.join('Medicoes', 'dadosXingo.csv'))
        data = pd.read_csv(path, ',', index_col=0, parse_dates=True)
        iha = IHA(data)
        return iha

    @staticmethod
    def read_iha(file):
        path = os.path.abspath(os.path.join('test_data', file))
        data = pd.read_csv(path, ';', index_col=0)
        return data

    def test(self, data, data2):
        for i in data.index:
            self.assertEqual(data.Means[i], data2.Means[i])
            self.assertEqual(data['Coeff. of Var.'][i], data2['Coeff. of Var.'][i])

    def test_mean_month(self):
        data = self.read_iha('Group1.csv')
        data2 = self.read().magnitude()
        self.test(data, data2)

    def test_moving_averages(self):
        data = self.read_iha('Group2.csv')
        data2 = self.read().magnitude_and_duration()
        self.test(data, data2)

    def test_year_water(self):
        year_water = self.read().flow.month_start_year_hydrologic("XINGO")
        self.assertEqual((9, 'SEP'), year_water, 'Year Water: %s, %s' % (9, 'SEP'))

    def test_days_julian(self):
        data2 = self.read().timing_extreme()
        data = self.read_iha('Group3.csv')
        self.test(data, data2)

    def test_pulse(self):
        data2 = self.read().frequency_and_duration(type_criterion=None, type_threshold="stationary", duration=0,
                                                   threshold_high=4813, threshold_low=569.5)
        data = self.read_iha('Group4.csv')
        self.test(data, data2)

    def test_rise_fall(self):
        data = self.read_iha('Group5.csv')
