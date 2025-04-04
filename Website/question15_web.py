import os
import streamlit as st
import pandas as pd
from pathlib import Path
from .question15_text import *
from .footer import add_footer
from Visualizations.question_15 import (
    plot_double_fields_player_combined,
    plot_double_fields_player,
    plot_player_average
)    
    
def question15_web():   
    def find_matching_file(folder_path, name):
        """
        Find a file in a folder that matches the given name."
        """
        folder = Path(folder_path)
        for file in folder.iterdir():
            if file.is_file() and file.stem == name:
                return file.name
        return None


    st.title("Player Stats")
    st.markdown("---")

    # List of players
    players = [
        "Rob Cross", "Luke Humphries", "Michael van Gerwen", "Stephen Bunting",
        "Gerwyn Price", "Nathan Aspinall", "Chris Dobey",
        "Gary Anderson", "James Wade", "Peter Wright", "Martin Schindler",
        "Luke Littler"
    ]

    # Player selection dropdown
    selected_player = st.selectbox("Select a Player", players)
    
    # Retrieve player data
    csv_file = "Data/player_data/male_players.csv"
    df = pd.read_csv(csv_file)
    df.fillna("No information", inplace=True)
    
    player_data = df[df["Name"] == selected_player].iloc[0]
    
    if player_data["Handedness"] == "Rechtshänder":
        player_data["Handedness"] = "Right-handed Player"
    else:
        player_data["Handedness"] = "Left-handed Player" 
        
    if player_data["Nationality"] == "Niederlande":
        player_data["Nationality"] = "Netherlands"
    elif player_data["Nationality"] == "Schottland":
        player_data["Nationality"] = "Scotland"
    elif player_data["Nationality"] == "Deutschland":
        player_data["Nationality"] = "Germany"

    # Display player information
    col1, col2 = st.columns([1, 1])

    with col1:
        # Display player profile
        st.header(player_data["Name"])
        st.write(f"**Nationality:** {player_data['Nationality']}")
        st.write(f"**Date of Birth:** {player_data['Geburtstag']}")
        st.write(f"**Playing since:** {player_data['Plays since']}")
        st.write(f"**Professional since:** {player_data['Profi since']}")
        st.write(f"**Handedness:** {player_data['Handedness']}")
        st.write(f"**Darts Used:** {player_data['Darts gramm']}")

    with col2:
        folder_path = "Website/Pictures Website/Player_Pictures"
        name = player_data["Name"].replace(" ", "_")
        image_name = find_matching_file(folder_path, name)
        image_path = os.path.join(folder_path, image_name)
        st.image(image_path, use_container_width=True) 

    st.markdown("---")
    st.subheader(
        "How does the performance of individual players change over time?"
    )

    with st.expander("Explanation"):
        st.write(explanation_15)
   
    fig = plot_double_fields_player(selected_player)
    st.plotly_chart(fig)
    st.write(first_description_15)
    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_15)
    
    st.markdown("---")
    double_fields = [f"D{i}" for i in range(1, 21)] + ["D25"]
    selected_double = st.selectbox(
        "Select a Double Field", 
        double_fields, 
        index=double_fields.index("D1")
    )
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
        
    # Call footer
    add_footer()