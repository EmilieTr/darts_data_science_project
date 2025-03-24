import streamlit as st
import pandas as pd
from .question9_text import *
from .footer import add_footer
from Visualizations.question_9 import plot_histogram

def question9_web():    
    st.header("9. How likely is it to throw a 180 after the opponent threw one?")
    
    df = pd.read_csv('Visualizations/question_9/180_stats.csv')    

    # DataFrame in Streamlit anzeigen
    st.dataframe(df)
    
    st.subheader("Histogram")
    fig = plot_histogram("Probability (%)")
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(first_graph_9)
        
    add_footer()