import streamlit as st
import pandas as pd
from .texts import *
from .footer import add_footer
from Visualizations.question_10 import plot_histogram

def question10_web():
    st.header("10. How likely are participants win a leg after throwing a 180 as first throw?") 
    
    df = pd.read_csv('Visualizations/question_10/180_stats.csv') 
    st.dataframe(df)
    
    st.subheader("Histogram")
    fig = plot_histogram("Probability (%)")
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(first_graph_10)
        
    add_footer()