import streamlit as st

def navigation():
    # Sidebar for Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Tournaments", "Matches", "Players", "Data Pipeline"])
    
    return page