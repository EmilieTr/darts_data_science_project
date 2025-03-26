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
    # Themenbereiche
    st.markdown(f'<div class="box"><b>Tournaments</b> <hr> {question_2} <br> {question_5} <br> {question_7}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="box"><b>Matches</b> <hr> {question_4} <br> {question_9} <br> {question_10}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="box"><b>Players</b> <hr> {question_1} <br> {question_6} <br> {question_15}</div>', unsafe_allow_html=True)

    '''st.markdown("""
    <div class="box">
        <a href="#section1">📚 Bildung und Lernen</a>
    </div>
    <div class="box">
        <a href="#section2">💻 Technologie und Innovation</a>
    </div>
    <div class="box">
        <a href="#section3">🌍 Umwelt und Nachhaltigkeit</a>
    </div>
    """, unsafe_allow_html=True)'''

    # Call function to add footer
    add_footer()