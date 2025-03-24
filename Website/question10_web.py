import streamlit as st
import pandas as pd
from .question10_text import *
from .footer import add_footer
from Visualizations.question_10 import plot_histogram
from Visualizations.question_10 import t_test

def question10_web():
    st.title("Winning legs vs. 180 openings")
    st.markdown("---")

    st.subheader("How likely are participants win a leg after throwing a 180 as first throw?") 
    with st.expander("Explanation"):
        st.write("Explanation")
    df = pd.read_csv('Visualizations/question_10/180_stats.csv') 
    st.dataframe(df)
    st.write("Hier kommt eine kurze Beschreibung vom Diagramm hin.")
    with st.expander("Interpretation and critical evaluation"):
        st.write("Interpretation and critical evaluation")

    fig = plot_histogram("Probability (%)")
    st.plotly_chart(fig)
    st.write("Hier kommt eine kurze Beschreibung vom Diagramm hin.")
    with st.expander("Interpretation and critical evaluation"):
        st.write("T-Test between European Tour and Majors")
        st.write(t_test())
        st.write(first_graph_10)
        
    
        
    add_footer()