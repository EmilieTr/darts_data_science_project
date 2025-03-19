import pandas as pd
import plotly.graph_objects as go
import re
import streamlit as st

def plot_winning_averages(selected_tournaments):
    #st.write(selected_tournaments)
    # List of all major tournaments
    major_tournaments_all = [
        "World Championship",
        "World Matchplay",
        "World Grand Prix",
        "Grand Slam",
        "Players Championship Finals",
        "World Cup",
        "World Series of Darts Finals",
    ]
    extra_tournaments_all = ["European Tour", "Players Championship", "World Series"]
    
    major_tournaments = []
    extra_tournaments = []
    only_one = False

    if len(selected_tournaments) == 1:
        only_one = True
    for tournament in selected_tournaments:
        if tournament in major_tournaments_all:
            major_tournaments.append(tournament)
        elif tournament in extra_tournaments_all:
            extra_tournaments.append(tournament)
    #st.write(major_tournaments)
    # Load CSV file
    file = 'Data/question 2/question2.csv'
    df = pd.read_csv(file)
    
    # Remove beginning spaces in column names
    df.columns = df.columns.str.strip()

    # Filter data without average and average < 10
    df_cleaned = df.dropna(subset=['Average'])
    df_cleaned = df_cleaned[df_cleaned['Average'] >= 10]
    
    # Filter data of majors and extra tournaments
    df_all = df_cleaned[
        df_cleaned['Tournament'].isin(major_tournaments_all) | 
        df_cleaned['Tournament'].str.startswith(tuple(extra_tournaments_all), na=False) & 
        ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
    ]

    if (major_tournaments + extra_tournaments) == (major_tournaments_all + extra_tournaments_all):
        df_selected = df_all
    elif only_one == True:
        # Filter data of majors and extra tournaments
        df_selected = df_cleaned[
            (df_cleaned['Tournament'] == selected_tournaments[0]) 
        ]
    elif extra_tournaments != "":
        # Filter data of majors and extra tournaments
        df_selected = df_cleaned[
            df_cleaned['Tournament'].isin(major_tournaments) |
            df_cleaned['Tournament'].str.startswith(tuple(extra_tournaments), na=False) & 
            ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
        ]
    else:
        df_selected = df_cleaned[
            df_cleaned['Tournament'].isin(major_tournaments) | 
            ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
        ]  
    #st.write(df_selected.head())
    # Normalize tournament names (remove numbers)
    def normalize_tournament_name(name):
        return re.sub(r'\d+', '', name).strip()  # Removes numbers and extra spaces

    df_selected['Tournament'] = df_selected['Tournament'].apply(normalize_tournament_name)
    df_all['Tournament'] = df_all['Tournament'].apply(normalize_tournament_name)
    #st.write(df_selected.head())
    # Convert dates into years
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], errors='coerce')
    df_selected['Date'] = pd.to_datetime(df_selected['Date'], errors='coerce')
    df_all['Date'] = pd.to_datetime(df_all['Date'], errors='coerce')

    df_cleaned['Year'] = df_cleaned['Date'].dt.year
    df_selected['Year'] = df_selected['Date'].dt.year
    df_all['Year'] = df_all['Date'].dt.year

    # Group data by year and calculate the average
    average_per_year = df_cleaned.groupby('Year')['Average'].mean()

    # Average per tournament and year
    df_selected = df_selected[df_selected['Year'] >= 2000]  # We only use data from 2000 onwards
    df_all = df_all[df_all['Year'] >= 2000]
    df_grouped = df_selected.groupby(['Year', 'Tournament'])['Average'].mean().reset_index()
    
    #st.write(df_grouped.head())
    # Create figure
    fig = go.Figure()
    
    #if (major_tournaments + extra_tournaments) == (major_tournaments_all + extra_tournaments_all) or extra_tournaments != "":
        # Create line for each major tournament
        #unique_tournaments = df_grouped['Tournament'].unique()
        # Loop over each selected tournament and add a line to the plot
    #st.write(selected_tournaments)
    for tournament in selected_tournaments:
        
        df_tournament = df_grouped[df_grouped['Tournament'] == tournament]
        #st.write(df_tournament)
        fig.add_trace(go.Scatter(
            x=df_tournament['Year'],
            y=df_tournament['Average'],
            mode='lines',
            name=tournament
        ))

    # Create line for total average of majors
    avg_all_majors = df_all.groupby('Year')['Average'].mean()
    fig.add_trace(go.Scatter(
        x=avg_all_majors.index,
        y=avg_all_majors.values,
        mode='lines+markers',
        line=dict(width=3, dash='dot'),
        name="Average of all majors"
    ))

    # Update layout
    fig.update_layout(
        title="Development of Average Scores Over the Years",
        xaxis_title="Year",
        yaxis_title="Average Score",
        legend_title="Tournaments",
        hovermode="x unified"
    )

    return fig

# Show Plot
#fig.show()
#plot_winning_averages("World Championship").show()