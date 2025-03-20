import pandas as pd
import plotly.graph_objects as go

def plot_winning_averages(selected_tournaments):
    # List of major and extra tournaments
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

    # Check if only one tournament is selected
    if len(selected_tournaments) == 1:
        only_one = True

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
        df_selected = df_cleaned[
            (df_cleaned['Tournament'] == selected_tournaments[0]) 
        ]
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
        # Create a translation table to remove digits (0-9)
        remove_digits = str.maketrans('', '', '0123456789')
        
        # Apply the translation to remove digits and strip leading/trailing whitespace
        return name.translate(remove_digits).strip()

    df_selected['Tournament'] = df_selected['Tournament'].apply(normalize_tournament_name)
    df_all['Tournament'] = df_all['Tournament'].apply(normalize_tournament_name)

    # Convert dates to years
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], errors='coerce')
    df_selected['Date'] = pd.to_datetime(df_selected['Date'], errors='coerce')
    df_all['Date'] = pd.to_datetime(df_all['Date'], errors='coerce')

    df_cleaned['Year'] = df_cleaned['Date'].dt.year
    df_selected['Year'] = df_selected['Date'].dt.year
    df_all['Year'] = df_all['Date'].dt.year

    # Calculate the average score per year
    average_per_year = df_cleaned.groupby('Year')['Average'].mean()

    # Filter data from 2000 onwards
    df_selected = df_selected[df_selected['Year'] >= 2000]
    df_all = df_all[df_all['Year'] >= 2000]

    # Group data by year and tournament, then calculate average scores
    df_grouped = df_selected.groupby(['Year', 'Tournament'])['Average'].mean().reset_index()
    
    # Create the plot
    fig = go.Figure()
    
    for tournament in selected_tournaments:
        df_tournament = df_grouped[df_grouped['Tournament'] == tournament]

        fig.add_trace(go.Scatter(
            x=df_tournament['Year'],
            y=df_tournament['Average'],
            mode='lines',
            name=tournament
        ))

    # Line for the average of all majors
    avg_all_majors = df_all.groupby('Year')['Average'].mean()
    fig.add_trace(go.Scatter(
        x=avg_all_majors.index,
        y=avg_all_majors.values,
        mode='lines+markers',
        line=dict(width=3, dash='dot'),
        name="Average of all majors"
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
