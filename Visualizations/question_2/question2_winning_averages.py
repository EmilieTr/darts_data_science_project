import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def plot_winning_averages(selected_tournaments, add_regression=False, add_std=False):
    # List of major and extra tournaments
    major_tournaments_all = [
        "World Championship", "World Matchplay", "World Grand Prix", "Grand Slam",
        "Players Championship Finals", "World Cup", "World Series of Darts Finals",
    ]
    extra_tournaments_all = ["European Tour", "Players Championship", "World Series"]
    
    major_tournaments = []
    extra_tournaments = []
    only_one = len(selected_tournaments) == 1

    # Classify tournaments into major and extra categories
    for tournament in selected_tournaments:
        if tournament in major_tournaments_all:
            major_tournaments.append(tournament)
        elif tournament in extra_tournaments_all:
            extra_tournaments.append(tournament)

    # Load CSV file
    file = 'Data/question 2/question2.csv'
    df = pd.read_csv(file)
    
    # Remove leading spaces in column names
    df.columns = df.columns.str.strip()

    # Filter out rows without an average or with an average < 10
    df_cleaned = df.dropna(subset=['Average'])
    df_cleaned = df_cleaned[df_cleaned['Average'] >= 10]
    
    # Filter data for major and extra tournaments
    df_all = df_cleaned[
        df_cleaned['Tournament'].isin(major_tournaments_all) | 
        df_cleaned['Tournament'].str.startswith(tuple(extra_tournaments_all), na=False) & 
        ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
    ]

    # Apply filters based on selected tournaments
    if (major_tournaments + extra_tournaments) == (major_tournaments_all + extra_tournaments_all):
        df_selected = df_all
    elif only_one:
        df_selected = df_cleaned[df_cleaned['Tournament'] == selected_tournaments[0]]
    elif extra_tournaments:
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

    def normalize_tournament_name(name):
        return name.translate(str.maketrans('', '', '0123456789')).strip()

    df_selected['Tournament'] = df_selected['Tournament'].apply(normalize_tournament_name)
    df_all['Tournament'] = df_all['Tournament'].apply(normalize_tournament_name)

    # Convert dates to years
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], errors='coerce')
    df_selected['Date'] = pd.to_datetime(df_selected['Date'], errors='coerce')
    df_all['Date'] = pd.to_datetime(df_all['Date'], errors='coerce')

    df_cleaned['Year'] = df_cleaned['Date'].dt.year
    df_selected['Year'] = df_selected['Date'].dt.year
    df_all['Year'] = df_all['Date'].dt.year

    # Filter data from 2000 onwards
    df_selected = df_selected[df_selected['Year'] >= 2000]
    df_all = df_all[df_all['Year'] >= 2000]

    # Group data by year and tournament, then calculate average scores
    df_grouped = df_selected.groupby(['Year', 'Tournament'])['Average'].mean().reset_index()
    
    # **Farben aus der Prism-Farbpalette**
    prism_colors = px.colors.qualitative.Prism
    color_map = {tournament: prism_colors[i % len(prism_colors)] for i, tournament in enumerate(df_grouped['Tournament'].unique())}
  
    # Create the plot
    fig = go.Figure()
    
    for tournament in selected_tournaments:
        df_tournament = df_grouped[df_grouped['Tournament'] == tournament]

        fig.add_trace(go.Scatter(
            x=df_tournament['Year'],
            y=df_tournament['Average'],
            mode='lines',
            name=tournament,
            line=dict(color=color_map.get(tournament, "gray"))
        ))

    # Line for the average of all majors
    avg_all_majors = df_all.groupby('Year')['Average'].mean()
    fig.add_trace(go.Scatter(
        x=avg_all_majors.index,
        y=avg_all_majors.values,
        mode='lines',
        line=dict(width=3, dash='dot', color="black"),
        name="Average of all majors",
    ))

    # **Regression Line**
    if add_regression:
        x_years = avg_all_majors.index.to_numpy()
        y_avg = avg_all_majors.values

        # Berechnung der linearen Regression (1. Grad)
        coeffs = np.polyfit(x_years, y_avg, deg=1)
        regression_line = np.poly1d(coeffs)

        fig.add_trace(go.Scatter(
            x=x_years,
            y=regression_line(x_years),
            mode="lines",
            line=dict(color="blue", width=2, dash="dash"),
            name="Regression Line"
        ))

    # **Standardabweichung**
    if add_std:
        min_year = avg_all_majors.index.min()
        std_per_year = df_cleaned[df_cleaned['Year'] >= min_year].groupby('Year')['Average'].std()

        fig.add_trace(go.Scatter(
            x=std_per_year.index.tolist() + std_per_year.index[::-1].tolist(),
            y=(avg_all_majors + std_per_year).tolist() + (avg_all_majors - std_per_year).tolist()[::-1],
            fill="toself",
            fillcolor="rgba(0, 0, 255, 0.2)",  # Blaue Transparenz
            line=dict(color="rgba(255,255,255,0)"),
            name="Standard Deviation"
        ))

    # Update layout with English labels
    fig.update_layout(
        title="Development of Average Scores Over the Years",
        xaxis_title="Year",
        yaxis_title="Average Score",
        legend_title="Tournaments",
        hovermode="x unified"
    )

    return fig

#plot_winning_averages(["World Championship"], True, True).show()