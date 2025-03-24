import streamlit as st
from .footer import add_footer

def data_pipeline_web():
    st.title("Data Pipeline")
    st.header("Our Process of data aquisition, data transformation, and data visualization.")
    
    file_path = "data_pipelining.txt"  # Passe den Pfad an
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        st.text(text)
    except FileNotFoundError:
        st.error("File not found.")

    # Call function to add footer
    add_footer()