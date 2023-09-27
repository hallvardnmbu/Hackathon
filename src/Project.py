import streamlit as st
import pandas as pd
import plotly.graph_objs as go

from helpers.model import Model

st.set_page_config(
    page_title= "Electricity app",
    page_icon= "<3"
)
navigation = st.sidebar.radio("Navigation", ["Home", "About"])

if navigation == "Home":
    st.image("./_static/Teamstream.jpeg", width=700)

    with st.expander("About the project"):
        hidden_text = (
            """In the context of the global shift towards renewable energy sources and 
            decentralized energy generation, there is a growing need for accurate forecasting of 
            energy feed-in times and quantities. The goal of this project is to design a 
            predictive algorith that determines optimal  energy feed-in timings for individual 
            power producers. By doing so, it enables  investment banks to assess the financial 
            implications and market dynamics  of increased decentralized energy contributions to 
            the grid."""
        )
        st.write(hidden_text)
    
    with st.expander("How to use"):
        st.markdown("**Battery capacity, kWh**")
        st.text("Enter the capacity of your battery")
        st.markdown("**Export capacity**")
        st.text("Enter how much power your battery can export per hour")

    st.title("Your battery")

    col1, col2 = st.columns(2)
    batteri_kap = col1.slider('Your battery in kWh', value=50, min_value=10, max_value=100)
    export_capacity = col2.slider('Export capasity kWh/h', min_value=10, max_value=100)

    st.text(f'To empty your battery you must export for'
            f' {round(batteri_kap/export_capacity, 2)} hours')

    st.title("When to export in the 'next' 24 hours")

    with st.spinner("Loading predictions..."):
        model = Model("../data/combined_data.csv")
        predictions_plot, predictions, times = model.predict(index=24)
        st.plotly_chart(predictions_plot)

    st.write(predictions)

elif navigation == "About":
    st.title("About the team")
    st.write("This page is created by Karen, Isabelle, Hallvard and Leo ")

