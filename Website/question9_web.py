import streamlit as st
import pandas as pd
from .texts import *
from .footer import add_footer
from Visualizations.question_9 import plot_histogram

def question9_web():    
    st.title("Consecutive 180s")
    st.markdown("---")
    st.subheader("How likely is it to throw a 180 after the opponent threw one?")
    with st.expander("Explanation"):
        st.write("Explanation")

    df = pd.read_csv('Visualizations/question_9/180_stats.csv')    

    # DataFrame in Streamlit anzeigen
    st.dataframe(df)
    st.text("Kurze Beschreibung der Ergebnisse im Diagramm.")
    with st.expander("Interpretaion and critical evaluation"):
        st.write("Interpretation and critical evaluation")
    fig = plot_histogram("Probability (%)")
    st.plotly_chart(fig)
    st. text("Kurze Beschreibung der Ergebnisse im Diagramm.")
    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_9)
        
    add_footer()