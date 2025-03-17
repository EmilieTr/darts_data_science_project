import pandas as pd
import plotly.graph_objects as go
import re

def plot_winning_averages():

    # List of all major tournaments
    major_tournaments = [
        "PDC World Darts Championship",
        "World Matchplay",
        "World Grand Prix (Darts)",
        "Masters of Darts",
        "US Open (Darts)", 
        "Grand Slam of Darts",
        "Players Championship Finals",
        "World Cup of Darts",
        "World Masters (PDC)",
        "World Series of Darts Finals",
        "Champions League of Darts",
    ]
    extra_tournaments = ("European Tour", "Players Championship", "World Series")

    # Load CSV file
    file = 'Data/question 2/question2.csv'
    df = pd.read_csv(file)
    # Remove beginning spaces in column names
    df.columns = df.columns.str.strip()

    # Filter data without average and average < 10
    df_cleaned = df.dropna(subset=['Average'])
    df_cleaned = df_cleaned[df_cleaned['Average'] >= 10]

    # Filter data of majors and extra tournaments
    df_selected = df_cleaned[
        df_cleaned['Tournament'].isin(major_tournaments) | 
        df_cleaned['Tournament'].str.startswith(extra_tournaments, na=False) & 
        ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
    ]

    # Normalize tournament names (remove numbers)
    def normalize_tournament_name(name):
        return re.sub(r'\d+', '', name).strip()  # Removes numbers and extra spaces

    df_selected['Tournament'] = df_selected['Tournament'].apply(normalize_tournament_name)

    # Convert dates into years
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], errors='coerce')
    df_selected['Date'] = pd.to_datetime(df_selected['Date'], errors='coerce')

    df_cleaned['Year'] = df_cleaned['Date'].dt.year
    df_selected['Year'] = df_selected['Date'].dt.year

    # Group data by year and calculate the average
    average_per_year = df_cleaned.groupby('Year')['Average'].mean()

    # Average per tournament and year
    df_selected = df_selected[df_selected['Year'] >= 2000]  # We only use data from 2000 onwards
    df_grouped = df_selected.groupby(['Year', 'Tournament'])['Average'].mean().reset_index()

    # Create figure
    fig = go.Figure()

    # Create line for each major tournament
    unique_tournaments = df_grouped['Tournament'].unique()
    for tournament in unique_tournaments:
        df_tournament = df_grouped[df_grouped['Tournament'] == tournament]
        
        fig.add_trace(go.Scatter(
            x=df_tournament['Year'],
            y=df_tournament['Average'],
            mode='lines',
            name=tournament
        ))

    # Create line for total average of majors
    avg_all_majors = df_selected.groupby('Year')['Average'].mean()
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
