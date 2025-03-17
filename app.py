import streamlit as st
import pandas as pd
from Visualizations.question_1 import question_1

# Sidebar für Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Participants", "Checkout Rates"])

# Daten laden
#df_participants = pd.read_csv('data/question5.csv')
#df_checkouts = pd.read_csv('data/question6.csv')

# Seite wechseln
if page == "Participants":
    st.title("Participants Over the Years")
    fig = question_1()
    st.plotly_chart(fig)