import streamlit as st
import pandas as pd
from .question9_text import *
from .footer import add_footer
from Visualizations.question_9 import plot_histogram

def question9_web():    
    st.title("Consecutive 180s")
    st.markdown("---")
    st.subheader("How likely is it to throw a 180 after the opponent threw one?")
    with st.expander("Explanation"):
        st.write(explanation_9)

    df = pd.read_csv('Visualizations/question_9/180_stats.csv')    
    st.write(first_description_9)

    # DataFrame in Streamlit anzeigen
    st.dataframe(df)
    st.write("Kurze Beschreibung der Ergebnisse im Diagramm.")
    with st.expander("Interpretaion and critical evaluation"):
        st.write("Interpretation and critical evaluation")
    fig = plot_histogram("Probability (%)")
    st.plotly_chart(fig)
    st.write(second_description_9)
    with st.expander("Interpretation and critical evaluation"):
        st.write(second_graph_9)
        
    add_footer()