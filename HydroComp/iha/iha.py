from HydroComp.iha.exceptions import NotStation
import pandas as pd
import calendar as cal
import plotly as py
from HydroComp.series.flow import Flow


class IHA:

    def __init__(self, data, month_water=None, station=None):
        self.flow = Flow(data)
        self.station = self.get_station(station)
        self.month_start = self.get_month_start(month_water)

    def rva(self):
        pass

    def metric_stats(self, group):
        mean = pd.DataFrame(group.mean(), columns=['Means'])
        cv = pd.DataFrame(group.std() / group.mean(), columns=['Coeff. of Var.'])
        stats = mean.combine_first(cv)
        return stats

    def get_station(self, station):
        if len(self.flow.data.columns.values) != 1:
            if station is None:
                raise NotStation("Station requirement")
            else:
                if station in self.flow.data.columns.values:
                    return station
                else:
                    raise NotStation("Not station")
        else:
            get_station = self.flow.data.columns.values[0]
            self.flow.data = pd.DataFrame(self.flow.data[get_station])

            return get_station

    def get_month_start(self, month_water):
        if month_water is None:
            return self.flow.month_start_year_hydrologic(station=self.station)
        else:
            return cal.month_abbr[month_water].upper()

    # <editor-fold desc="Group 1: Magnitude of monthly water conditions">
    def magnitude(self):
        years = self.flow.data.groupby(pd.Grouper(freq='A'))
        data = pd.DataFrame()
        for year in years:
            aux = year[1].groupby(pd.Grouper(freq='M')).mean()
            df = pd.DataFrame({year[0].year: {
                cal.month_name[i.month]: aux[self.station][i] for i in aux[self.station].index}})
            data = data.combine_first(df)
        mean_months = data.T

        return self.metric_stats(mean_months)
    # </editor-fold">

    # <editor-fold desc="Group 2: Magnitude and Duration of annual extreme water conditions">
    def magnitude_and_duration(self):
        aver_data = pd.DataFrame()
        for i in [1, 3, 7, 30, 90]:
            ave_max = self.flow.data.rolling(window=i).mean().groupby(pd.Grouper(freq='A')).max()
            ave_min = self.flow.data.rolling(window=i).mean().groupby(pd.Grouper(freq='A')).min()
            years = ave_max.index.year
            df1 = pd.DataFrame(pd.Series(data=ave_min[self.station].values, name='%s-day minimum' % i, index=years))
            df2 = pd.DataFrame(pd.Series(data=ave_max[self.station].values, name='%s-day maximum' % i, index=years))
            aver_data = aver_data.combine_first(df1)
            aver_data = aver_data.combine_first(df2)
            if i == 7:
                mean_year = self.flow.data[self.station].groupby(pd.Grouper(freq='A')).mean().values
                base_flow = pd.DataFrame(pd.Series(data=ave_min[self.station].values / mean_year,
                                                   name='Base flow index', index=years))
                aver_data = aver_data.combine_first(base_flow)

        dic_zero = {i[0].year: i[1].loc[i[1][self.station].values == 0].sum()
                    for i in self.flow.data.groupby(pd.Grouper(freq='A'))}

        magn_and_duration = aver_data.combine_first(pd.DataFrame(pd.Series(data=dic_zero, name='Number of zero days')))

        return self.metric_stats(magn_and_duration)
    # </editor-fold>

    # <editor-fold desc="Group 3: Timing of annual extreme water conditions">

    def timing_extreme(self):

        day_julian_max = pd.DatetimeIndex(self.flow.data[self.station].groupby(pd.Grouper(freq='A')).idxmax().values)
        day_julian_min = pd.DatetimeIndex(self.flow.data[self.station].groupby(pd.Grouper(freq='A')).idxmin().values)

        df_day_julian_max = pd.DataFrame(list(map(int, day_julian_max.strftime("%j"))), index=day_julian_max.year,
                                         columns=["Date of maximum"])
        df_day_julian_min = pd.DataFrame(list(map(int, day_julian_min.strftime("%j"))), index=day_julian_min.year,
                                         columns=["Date of minimum"])

        # combine the dfs of days julian
        timing_extreme = df_day_julian_max.combine_first(df_day_julian_min)
        return self.metric_stats(timing_extreme)
    # </editor-fold>

    # <editor-fold desc="Group 4: Frequency and duration of high and low pulses">
    # Obs.: Ver se pode ser usado ano hidrológico
    def __aux_frequency_and_duration(self, events):
        name = {'flood': 'High', 'drought': 'Low'}
        type_event = events.type_event
        duration_pulse = pd.DataFrame(events.peaks.groupby(pd.Grouper(freq='A')).Duration.mean()).rename(
            columns={"Duration": '{} pulse duration'.format(name[type_event])})

        pulse = pd.DataFrame(events.peaks.groupby(pd.Grouper(freq='A')).Duration.count()).rename(
            columns={"Duration": '{} pulse count'.format(name[type_event])})

        group = duration_pulse.combine_first(pulse)
        threshold = pd.DataFrame(pd.Series(events.threshold, name="{} Pulse Threshold".format(name[type_event])))
        group = group.combine_first(threshold)
        return group

    def frequency_and_duration(self, type_threshold, type_criterion, threshold_high, threshold_low, **kwargs):
        events_high = self.flow.parcial(station=self.station, type_threshold=type_threshold, type_event="flood",
                                        type_criterion=type_criterion, value_threshold=threshold_high)
        frequency_and_duration_high = self.__aux_frequency_and_duration(events_high)

        events_low = self.flow.parcial(station=self.station, type_event='drought', type_threshold=type_threshold,
                                       type_criterion=type_criterion, value_threshold=threshold_low)
        frequency_and_duration_low = self.__aux_frequency_and_duration(events_low)

        frequency_and_duration = frequency_and_duration_high.combine_first(frequency_and_duration_low)

        return self.metric_stats(frequency_and_duration)

    # </editor-fold>

    # <editor-fold desc="Group 5: Rate and frequency of water condition changes">
    def rate_and_frequency(self):
        pass
    # </editor-fold>
