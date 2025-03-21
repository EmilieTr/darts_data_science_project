import streamlit as st
from Website.texts import *
from Website.navigation import navigation
from Website.home import home
from Website.question2_web import question2_web
from Website.question5_web import question5_web
from Website.question7_web import question7_web
from Website.question15_web import question15_web
from Website.question4_web import question4_web
from Website.question1_web import question1_web
from Website.question6_web import question6_web
from Website.question9_web import question9_web
from Website.question10_web import question10_web
from Website.data_pipeline_web import data_pipeline_web

page = navigation()

# Change page
if page == "Home":
    home()

elif page == "Tournaments":
    subpage = st.sidebar.radio(
        "Tournament Data",
        [
            "2 Averages",
            "5 Prize Money and Participants",
            "7 Host Country vs. Nationality"
        ]
    )

    # Question 2
    if subpage == "2 Averages":
        question2_web()
        
    # Question 5
    elif subpage == "5 Prize Money and Participants":
        question5_web()
        
    # Question 7
    if subpage == "7 Host Country vs. Nationality":
        question7_web()
        
elif page == "Matches":
    subpage = st.sidebar.radio(
        "Player Data", 
        [
            "4 Popular Double Fields",
            "9 Consecutive 180s",
            "10 Winning Legs vs. 180 openings"
        ]
    )
    
    # Question 4
    if subpage == "4 Popular Double Fields":
        question4_web()
        
        # Question 9    
    elif subpage == "9 Consecutive 180s":
        question9_web()
        
    # Question 10     
    elif subpage == "10 Winning Legs vs. 180 openings":  
        question10_web()

elif page == "Players":
    subpage = st.sidebar.radio(
        "Player Data", 
        [
            "1 Averages of the Best",
            "6 Rankings vs. Properties",
            "15 Player Stats"
        ]
    )
    
    # Question 15
    if subpage == "15 Player Stats":
        question15_web()

    # Question 1
    elif subpage == "1 Averages of the Best":
        question1_web()

    # Question 6
    elif subpage == "6 Rankings vs. Properties":
        question6_web()

elif page == "Data Pipeline":
    data_pipeline_web()