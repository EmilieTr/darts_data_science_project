import streamlit as st
import pandas as pd
from .texts import *
from .footer import add_footer

def question9_web():    
    st.header("9. How likely is it to throw a 180 after the opponent threw one?")
    
    df = pd.read_csv('Visualizations/question_9/180_stats.csv')
    st.dataframe(df)

    with st.expander("Interpretation"):
        st.write(first_graph_9)
        
    add_footer()