import plotly.graph_objs as go

from HydroComp.graphics.hydrogram_biuld import HydrogramBiuld


class HydrogramAnnual(HydrogramBiuld):

    def __init__(self, data, peaks):
        super().__init__()
        self.data = data
        self.peaks = peaks

    def plot(self, ype_criterion=None):
        bandxaxis = go.layout.XAxis(title="Data")
        bandyaxis = go.layout.YAxis(title="Vazão(m³/s)")

        layout = dict(title="Hidrograma Série Máximas Anuais",
                      #width=1890, height=827,
                      xaxis=bandxaxis, yaxis=bandyaxis,
                      font=dict(family='Time New Roman', size=18, color='rgb(0,0,0)')
                      )

        data = list()
        data.append(self._plot_one(self.data))
        data.append(self._plot_event_peaks())

        fig = dict(data=data, layout=layout)
        return fig, data

    def _plot_event_peaks(self):

        point_peak = go.Scatter(
            x=self.peaks.index,
            y=self.data[self.data.columns.values[0]].loc[self.peaks.index].values,
            name="Peaks",
            mode='markers',
            marker=dict(size=8,
                        color='rgb(128, 128, 128)',
                        line=dict(width=1,
                                  color='rgb(0, 0, 0)'),),
            opacity=1)

        return point_peak
