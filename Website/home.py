import streamlit as st
from .texts import *
from .footer import add_footer

def home():
    # Set page title and icon
    st.title("Welcome to the Darts Data Science Project! 🎯")
    st.header("Dive into the analysis and uncover the hidden patterns in the world of darts!")

    # Introduction
    st.subheader(introduction)
    with st.expander("Game Explanation"):
        st.write(darts_explanation)

    # Research Questions
    st.subheader("Research Questions Explored")
    st.write("**Subtopic: Tournament Data**")
    st.write("- How do the averages of tournaments vary over time?")
    st.write("- How does the price money and number of participants vary over time?")
    st.write("- How does the country a tournament is held in correlate to the success of players?")
    st.write("**Subtopic: Player Data**")
    st.write("- How does the performance of players in general change over time?")
    st.write("- How does the performance of individual players change over time?")
    st.write("- How does age, nationality and handiness effects the rankings?")
    st.write("- Is there a difference between a player's team performance and single performance?")
    st.write("- How likely is it to throw 180 points after there was another 180 points thrown?")
    st.write("- How likely are participants to win a leg after throwing 180 points as first throw?")

    # Call function to add footer
    add_footer()