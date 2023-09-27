import streamlit as st
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
        width=700,
        height=500)

    # Create a Plotly figure and add the trace with the layout
    fig = go.Figure(data=[trace], layout=layout)

    # Display the plot
    #fig.show()

    return fig 


fig= datafunc("../test.csv",["Dato/klokkeslett","NO5"])


##Creating website


st.set_page_config(
    page_title= "Electricity app",
    page_icon= "<3"
)
# Create a navigation bar using radio buttons
navigation = st.sidebar.radio("Navigation", ["Home", "Calculator", "About"])

# Page content based on navigation choice
if navigation == "Home":
    st.title("TEAM STREAM")
    st.write("Welcome to our Electricity Price Forecaster app")
    st.text("Hackathon Case 1 - Electricity Price Forecasting")
    st.markdown("## Formål")
    st.plotly_chart(fig)

elif navigation == "Page 1":
    st.title("Calulator")
    st.write("This is Page 1. You can put your content here.")
elif navigation == "Page 2":
    st.title("Page 2")
    st.write("This is Page 2. You can put different content here.")

st.title('Batteri funksjonalitet')

st.subheader('Batterikapasitet, kWh')
batteri_kap = st.slider('Velg din batterikapasitet', value= 50,min_value=10, max_value=100)



st.text(f'Ditt batteri inneholder maksimalt {batteri_kap}')

st.subheader('Hvor mye strøm kan ditt batteri eksportere per time?')
strøm_output = st.slider('Eksport kapasitet', min_value=10, max_value=100)

st.text(f'Du kan da eksportere strøm i {batteri_kap/strøm_output}')

