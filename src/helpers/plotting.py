import pandas as pd
import plotly.graph_objs as go


def optimal_times(hours, predictions, times):
    _times = {}
    for i, pred in enumerate(predictions):
        _times[times.iloc[i]] = pred

    _times = dict(sorted(_times.items(), key=lambda x: x[1], reverse=True))
    _sell_times = [k for k, v in _times.items()]
    sell_times = [pd.to_datetime(_sell_times[i]) for i in range(hours)]

    intervals = [(_time, _time + pd.Timedelta(hours=1)) for _time in sell_times]

    return intervals


def plot_shading(spot, predictions, times, shading):
    """
    Plots the shading of the area below the graph.

    Parameters
    ----------
    spot : list
        The spot price in the interval.
    times : pd.Series
        The times.
    shading : list of tuple
        List of tuples with the start and end time of the shading.
    """

    data = pd.DataFrame({"spot": spot, "times": times, "predictions": predictions})
    data = data.set_index("times")

    fig = go.Figure()

    for shade in shading:
        # interval = pd.date_range(shade[0], shade[1], freq="H")
        i, j = shade
        try:
            fig.add_trace(
                go.Scatter(x=[i, j], y=[data.loc[i]["predictions"],
                                        data.loc[j]["predictions"]],
                           name="Spot price",
                           fill="tozeroy", fillcolor="#D3D3D3", showlegend=False,
                           mode="none", opacity=0.3)
            )
        except KeyError:
            pass

    fig.add_trace(
        go.Scatter(x=data.index, y=data["predictions"],
                   name='Predicted', line={"color": "#708090"}))
    fig.add_trace(
        go.Scatter(x=data.index, y=data["spot"],
                   name='Actual',
                   line={"dash": 'dash', "color": "#FF6347"}))
    fig.update_xaxes(tickangle=45, tickformat='%Y-%m-%d %H:%M')
    fig.update_yaxes(title_text="NO2")

    return fig
