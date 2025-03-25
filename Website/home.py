import streamlit as st
from .footer import add_footer
from .texts import *

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
    st.write("**Subtopic: Tournaments**")
    st.write(question_2)
    st.write(question_5)
    st.write(question_7)
    st.write("**Subtopic: Matches**")
    st.write(question_4)
    st.write(question_9)
    st.write(question_10)
    st.write("**Subtopic: Players**")
    st.write(question_1)
    st.write(question_6)
    st.write(question_15)

    # Call function to add footer
    add_footer()