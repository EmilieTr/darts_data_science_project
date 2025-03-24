import streamlit as st
import pandas as pd
from .question15_text import *
from .footer import add_footer
from Visualizations.question_15 import (
    plot_double_fields_player_combined,
    plot_double_fields_player,
    plot_player_average
)    
    
def question15_web():   
    st.title("Player Stats")
    st.markdown("---")
     # Load a list of players from CSV or define manually
    players = [
        "Luke Humphries", "Luke Littler", "Michael van Gerwen",
        "Phil Taylor", "Stephen Bunting", "Rob Cross", "Gerwyn Price",
        "Nathan Aspinall", "Chris Dobey", "Gary Anderson", "James Wade",
        "Peter Wright", "Martin Schindler"
    ]  # Replace with real names or load from a file
    
    # Dropdowns for selecting player and double field
    selected_player = st.selectbox("Select a Player", players)
    
    # Retrieve player data
    csv_file = "Data/question 6/male_players.csv"
    df = pd.read_csv(csv_file)
    player_data = df[df["Name"] == selected_player].iloc[0]
    if player_data["Handedness"] == "Rechtshänder":
        player_data["Handedness"] = "Right-handed Player"
    else:
        player_data["Handedness"] = "Left-handed Player"

    # Display player profile
    st.header(player_data["Name"])
    st.write(f"**Nationality:** {player_data['Nationality']}")
    st.write(f"**Date of Birth:** {player_data['Geburtstag']}")
    st.write(f"**Playing since:** {player_data['Plays since']}")
    st.write(f"**Professional since:** {player_data['Profi since']}")
    st.write(f"**Handedness:** {player_data['Handedness']}")
    st.write(f"**Darts Used:** {player_data['Darts gramm']}")
    st.markdown("---")
    st.subheader("How does the performance of individual players change over time?")

    with st.expander("Explanation"):
        st.write(explanation_15)
    
   
    fig = plot_double_fields_player(selected_player)
    st.plotly_chart(fig)
    st.write(first_description_15)
    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_15)
    
    st.markdown("---")
    double_fields = [f"D{i}" for i in range(1, 21)] + ["D25"]  # Double fields
    selected_double = st.selectbox("Select a Double Field", double_fields)
    st.markdown("---")
    
    fig = plot_double_fields_player_combined(selected_player, selected_double)
    st.plotly_chart(fig)
    st.write(second_description_15)
    with st.expander("Interpretation and critical evaluation"):
        st.write(second_graph_15)
    
    fig = plot_player_average(selected_player)
    st.plotly_chart(fig)
    st.write(third_description_15)
    with st.expander("Interpretation and critical evaluation"):
        st.write(third_graph_15)
        
    # Call function to add footer
    add_footer()