import streamlit as st
import pandas as pd
from Visualizations.question_1 import question_1
from Visualizations.question_2 import question_2
from Visualizations.question_4 import question_4
from Visualizations.question_5 import question_5
#from Visualizations.question_6 import question_1
from Visualizations.question_7 import question_7
from Visualizations.question_8 import question_8
#from Visualizations.question_9 import question_1

# Sidebar für Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Development of Tournaments", "Strategies and Tactics", "Players"])

# Seite wechseln  
if page == "Development of Tournaments":
    subpage = st.sidebar.radio("", ["Development of Tournaments", "Price Money and Participants at WC"])
    
    if subpage == "Averages throughout the years":
        st.title("Participants Over the Years")
        fig = question_2()
        st.plotly_chart(fig)
    elif subpage == "Price Money and Participants at WC":
        st.title("Participants Over the Years")
        fig = question_5()
        st.plotly_chart(fig)
        
elif page == "Strategies and Tactics":
    subpage = st.sidebar.radio("Strategies and Tactics", ["Location of Tournament and Winner Nationality", "Team vs. Single", "Double Fields"])
    
    if subpage == "Location of Tournament and Winner Nationality":
        st.title("Participants Over the Years")
        fig = question_7()
        st.plotly_chart(fig)
    elif subpage == "Team vs. Single":
        st.title("Participants Over the Years")
        fig = question_8()
        st.plotly_chart(fig)
    elif subpage == "Double Fields":
        st.title("Participants Over the Years")
        fig = question_4()
        st.plotly_chart(fig)
        
elif page == "Players":
    subpage = st.sidebar.radio("Players", ["Averages of Best Players", "Rankings vs Properties"])
    
    if subpage == "Averages of Best Players":
        st.title("Participants Over the Years")
        fig = question_1()
        st.plotly_chart(fig)
    elif subpage == "Rankings vs Properties":
        st.title("Participants Over the Years")
        fig = question_6()
        st.plotly_chart(fig)
        
    