import streamlit as st
from .footer import add_footer

def home():
    # Set page title and icon
    st.title("Welcome to the Darts Data Science Project! 🎯")
    st.markdown("---")
    st.header("Dive into the analysis and uncover the hidden patterns in the world of darts!")

    # Introduction
    st.write("This project dives into the world of darts using data science techniques to uncover fascinating insights. Below you will find a short explanation for the game to give you an understanding and context to view the analysis results in. There is also a subpage to explain the data pipeline of our data science project, so the efforts to get to these results can be easily tracked.")
    
    file_path = "darts_explanation.txt"  # Passe den Pfad an
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        with st.expander("Game Explanation"):
            st.write(text)
    except FileNotFoundError:
        st.error("File not found.")

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