import pandas as pd
import numpy as np
import plotly.graph_objs as go

def datafunc(filename,cols):

    #cols = list with columnames as string ["Tidsintervall", "Spotpris"]
    data= pd.read_csv(filename,encoding="UTF-8", sep=";", usecols=cols)

    #creates empty dictionary
    d={}
    
    for index, row in data.iterrows():
        timeint= row[cols[0]]
        Spotpris= row[cols[1]]
        Spotpris= float(Spotpris.replace(",","."))

        d[timeint]=Spotpris
    

    sorted_dict = dict(sorted(d.items(),key=lambda x:(x[1]), reverse=True)) 
    
    #plotting
    data = d
    xs = []
    ys = []

    for key, value in data.items():
        xs.append(key)
        ys.append(value)

    # Create a Plotly scatter plot trace
    trace = go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='red'))

    # Create the layout for the plot
    layout = go.Layout(
        title='Spotpris Over Tid',
        xaxis=dict(title='Klokkeslett'),
        yaxis=dict(title='Spotpris'),
        showlegend=False,
        width=800,
        height=600)

    # Create a Plotly figure and add the trace with the layout
    fig = go.Figure(data=[trace], layout=layout)

    # Display the plot
    fig.show()




datafunc("test.csv",["Dato/klokkeslett","NO5"])