import os
import streamlit as st

from .footer import add_footer
from .texts import *

def home():
    """
    Render the home page of the Darts Data Science Project.
    """
    col1, col2 = st.columns([1, 1])

    with col1:
        st.title("Welcome to the Darts Data Science Project!")
        st.markdown("---")

    with col2:
        folder_path = "Website/Pictures Website"
        image_name = "dartboard.png"
        image_path = os.path.join(folder_path, image_name)
        st.image(image_path, use_container_width=True) 
    
    st.header(
        "Dive into the analysis and uncover the hidden patterns "
        "in the world of darts!"
    )
    
    # Introduction
    st.write(
        "This project dives into the world of darts using data science "
        "techniques to uncover fascinating insights. Below you will find a "
        "short explanation for the game to give you an understanding and "
        "context to view the analysis results in. There is also a subpage "
        "to explain the data pipeline of our data science project, so the "
        "efforts to get to these results can be easily tracked."
    )

    file_path = "darts_explanation.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        with st.expander("Game Explanation"):
            st.write(text)
    except FileNotFoundError:
        st.error("File not found.")
    st.markdown('---')
    # Research Questions
    st.subheader("Research Questions Explored")
    st.markdown(
        f'<div class="box test"><b>Tournaments</b><div class="box test"><b>Matches</b><div class="box test"><b>Players</b></div></div></div>',
        unsafe_allow_html=True
    )
    
    
    # Subtopics
    st.markdown(
        f'<div class="box"><b>Tournaments</b> <hr> {question_2} <br> '
        f'{question_5} <br> {question_7}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="box"><b>Matches</b> <hr> {question_4} <br> '
        f'{question_9} <br> {question_10}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="box"><b>Players</b> <hr> {question_1} <br> '
        f'{question_6} <br> {question_15}</div>',
        unsafe_allow_html=True
    )
    
    # Call footer
    add_footer()