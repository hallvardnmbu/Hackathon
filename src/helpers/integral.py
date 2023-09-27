import pandas as pd
import plotly.graph_objs as go


def plot_shading(spot, times, shading):
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
    data = pd.DataFrame({"Date": times, "NO2": spot})
    data.set_index("Date", inplace=True)

    fig = go.Figure()
    for shade in shading:
        interval = pd.date_range(shade[0], shade[1], freq="H")
        i = interval[0]
        for j in interval[1]:
            fig.add_trace(
                go.Scatter(x=[i, j], y=[data.loc[i], data.loc[j]], name="Spot price",
                           fill="tozeroy", fillcolor="firebrick", showlegend=False,
                           mode="none")
            )
            i = j

    fig.add_trace(
        go.Scatter(x=spot.index, y=spot, name="Spot price",
                   line=dict(color="firebrick", width=2))
    )

    return fig
