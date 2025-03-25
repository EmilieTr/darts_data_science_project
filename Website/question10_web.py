import streamlit as st
import pandas as pd
from .question10_text import *
from .footer import add_footer
from Visualizations.question_10 import (plot_histogram, t_test)

def question10_web():
    st.title("Winning legs vs. 180 openings")
    st.markdown("---")
    st.subheader(
        "How likely are participants to win a leg after throwing a 180 as first throw?"
    )

    with st.expander("Explanation"):
        st.write(explanation_10)

    df = pd.read_csv('Visualizations/question_10/180_stats.csv') 
    st.dataframe(df)
    st.write(first_description_10)
    
    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_10)

    fig = plot_histogram("Probability (%)")
    st.plotly_chart(fig)
    st.write(second_description_10)
    
    with st.expander("Interpretation and critical evaluation"):
        st.write("T-Test between European Tour and Majors")
        st.write(t_test())
        st.write(second_graph_10)
    
    # Call footer
    add_footer()