import streamlit as st
import pandas as pd
from .texts import *
from .footer import add_footer
from Visualizations.question_15 import (
    plot_double_fields_player_combined,
    plot_double_fields_player,
    plot_player_average
)    
    
def question15_web():   
    st.header(
        "15. How does the performance of individual players change over "
        "time?"
    )

    with st.expander("Interpretation"):
        st.write(first_graph_15)
    
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
    
    st.subheader(f"Double Field Values of {selected_player}")
    fig = plot_double_fields_player(selected_player)
    st.plotly_chart(fig)
    
    double_fields = [f"D{i}" for i in range(1, 21)] + ["D25"]  # Double fields
    selected_double = st.selectbox("Select a Double Field", double_fields)
    
    st.subheader(
        f"Throws on {selected_double} and its Double Quota "
        f"for {selected_player}"
    )
    fig = plot_double_fields_player_combined(selected_player, selected_double)
    st.plotly_chart(fig)
    
    st.subheader(
        f"Averages for {selected_player}"
    )
    fig = plot_player_average(selected_player)
    st.plotly_chart(fig)

    # Call function to add footer
    add_footer()