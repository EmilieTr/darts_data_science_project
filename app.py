import streamlit as st
from Website.texts import *
from Website.navigation import navigation
from Website.home import home
from Website.question1_web import question1_web
from Website.question2_web import question2_web
from Website.question4_web import question4_web
from Website.question5_web import question5_web
from Website.question6_web import question6_web
from Website.question7_web import question7_web
from Website.question9_web import question9_web
from Website.question10_web import question10_web
from Website.question15_web import question15_web
from Website.data_pipeline_web import data_pipeline_web

# Sidebar for Navigation
# --- Sidebar Styling ---
st.markdown("""
    <style>
        /* Sidebar-Hintergrund */
        [data-testid="stSidebar"] {
            background-color: #F4F0EC;
            padding: 20px;
        }
        
        /* Allgemeine Sidebar-Schriftfarbe (ohne Buttons) */
        [data-testid="stSidebar"] * {
            color: black;
            font-size: 16px;
        }
        
        /* Breite der Sidebar */
        section[data-testid="stSidebar"] {
            width: 280px !important;
        }

        /* Button-Styling */
        .stButton>button {
            background: none;
            color: black !important;
            border-radius: 8px;
            border: 1px solid #86a47c;
            padding: 10px;
            width: 100%;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #86a47c;
        }

        /* Expander-Styling */
        [data-testid="stExpander"] {
            background-color: #FAF9F6;
            border-radius: 8px;
            padding: 5px;
        }
        /* Entire MultiSelect widget */
        .stMultiSelect {
            background-color: #FAF9F6; /* Background color */
            border-radius: 8px; /* Rounded corners */
            padding: 5px; /* Padding */
        }
    </style>
""", unsafe_allow_html=True)
st.sidebar.title("Darts")

# Initialisiere den Session State für die Navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Funktion zum Wechseln der Seite
def navigate(page_name):
    st.session_state.page = page_name

# Home-Button separat
if st.sidebar.button("Home", key="home"):
    navigate("Home")

# Expander für Tournaments
with st.sidebar.expander("Tournaments"):
    if st.button("2 Averages", key="averages_2"):
        navigate("2 Averages")
    if st.button("5 Prize Money and Participants", key="prize_money_5"):
        navigate("5 Prize Money and Participants")
    if st.button("7 Host Country vs. Nationality", key="host_vs_nationality_7"):
        navigate("7 Host Country vs. Nationality")

# Expander für Matches
with st.sidebar.expander("Matches"):
    if st.button("4 Popular Double Fields", key="double_fields_4"):
        navigate("4 Popular Double Fields")
    if st.button("9 Consecutive 180s", key="consecutive_180s_9"):
        navigate("9 Consecutive 180s")
    if st.button("10 Winning Legs vs. 180 openings", key="winning_legs_10"):
        navigate("10 Winning Legs vs. 180 openings")

# Expander für Players
with st.sidebar.expander("Players"):
    if st.button("1 Averages of the Best", key="best_averages_1"):
        navigate("1 Averages of the Best")
    if st.button("6 Rankings vs. Properties", key="rankings_vs_properties_6"):
        navigate("6 Rankings vs. Properties")
    if st.button("15 Player Stats", key="player_stats_15"):
        navigate("15 Player Stats")

# Data Pipeline separat
if st.sidebar.button("Data Pipeline", key="data_pipeline"):
    navigate("Data Pipeline")

subpage = st.session_state.page
if subpage == "Home":
    home()
# Question 2
if subpage == "2 Averages":
    question2_web()
        
# Question 5
elif subpage == "5 Prize Money and Participants":
    question5_web()
    
# Question 7
if subpage == "7 Host Country vs. Nationality":
    question7_web()   
    
# Question 4
if subpage == "4 Popular Double Fields":
    question4_web()
    
    # Question 9    
elif subpage == "9 Consecutive 180s":
    question9_web()
    
# Question 10     
elif subpage == "10 Winning Legs vs. 180 openings":  
        question10_web()
    
# Question 15
if subpage == "15 Player Stats":
    question15_web()

# Question 1
elif subpage == "1 Averages of the Best":
    question1_web()

# Question 6
elif subpage == "6 Rankings vs. Properties":
    question6_web()

# Data Pipeline
elif subpage == "Data Pipeline":
    data_pipeline_web()