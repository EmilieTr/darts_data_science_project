import streamlit as st
from .texts import *
from .footer import add_footer

def data_pipeline_web():
    st.title("Data Pipeline")
    st.header("Our Process of data aquisition, data transformation, and data visualization.")
    st.write(data_pipeline)

    # Call function to add footer
    add_footer()