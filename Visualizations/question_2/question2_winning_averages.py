import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def plot_winning_averages(
    selected_tournaments,
    add_regression=False,
    add_std=False,
    apply_all=False
):
    """
    Plot winning averages over time for selected tournaments.
    """
    # Handle empty tournament selection
    if not selected_tournaments and apply_all==False:
        fig = go.Figure()
        fig.update_layout(
            title="Development of Average Scores over Time",
            xaxis_title="Year",
            yaxis_title="Average Score",
            legend_title="Tournaments",
            hovermode="x unified"
        )

        return fig
    

    def custom_index_order(n):
        """
        Generate a custom color index order."
        """
        result = []
        sequence = [0, 5, 2, 3, 6, 10, 8, 4, 7]
        result = (sequence * ((n // len(sequence)) + 1))[:n]

        return result

    # Define tournament categories
    major_tournaments_all = [
        "World Championship", "World Matchplay", "World Grand Prix",
        "Grand Slam", "Players Championship Finals", "World Cup",
        "World Series of Darts Finals",
    ]
    extra_tournaments_all = [
        "European Tour", "Players Championship", "World Series"
    ]

    # Categorize selected tournaments
    major_tournaments = []
    extra_tournaments = []
    only_one = len(selected_tournaments) == 1

    for tournament in selected_tournaments:
        if tournament in major_tournaments_all:
            major_tournaments.append(tournament)
        elif tournament in extra_tournaments_all:
            extra_tournaments.append(tournament)

    # Load CSV file
    file = 'Data/tournaments_averages.csv'
    df = pd.read_csv(file)

    # Remove leading spaces from column names
    df.columns = df.columns.str.strip()

    # Filter out invalid data
    df_cleaned = df.dropna(subset=['Average'])
    df_cleaned = df_cleaned[df_cleaned['Average'] >= 10]

    # Apply tournament filters
    df_all = df_cleaned[
        df_cleaned['Tournament'].isin(major_tournaments_all) |
        df_cleaned['Tournament'].str.startswith(
            tuple(extra_tournaments_all), na=False
        ) &
        ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
    ]

    # Apply filters based on selected tournaments
    if apply_all:
        df_selected = df_all
    elif (major_tournaments + extra_tournaments) == (
        major_tournaments_all + extra_tournaments_all
    ):
        df_selected = df_all
    elif only_one:
        df_selected = df_cleaned[
            df_cleaned['Tournament'] == selected_tournaments[0]
        ]
    elif extra_tournaments:
        df_selected = df_cleaned[
            df_cleaned['Tournament'].isin(major_tournaments) |
            df_cleaned['Tournament'].str.startswith(
                tuple(extra_tournaments), na=False
            ) &
            ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
        ]
    else:
        df_selected = df_cleaned[
            df_cleaned['Tournament'].isin(major_tournaments) &
            ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
        ]

    # Normalize tournament names by removing digits
    def normalize_tournament_name(name):
        return name.translate(
            str.maketrans('', '', '0123456789')
        ).strip()

    df_selected['Tournament'] = (
        df_selected['Tournament'].apply(normalize_tournament_name)
    )
    df_all['Tournament'] = (
        df_all['Tournament'].apply(normalize_tournament_name)
    )

    # Convert dates to datetime and extract the year
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], errors='coerce')
    df_selected['Date'] = pd.to_datetime(df_selected['Date'], errors='coerce')
    df_all['Date'] = pd.to_datetime(df_all['Date'], errors='coerce')

    df_cleaned['Year'] = df_cleaned['Date'].dt.year
    df_selected['Year'] = df_selected['Date'].dt.year
    df_all['Year'] = df_all['Date'].dt.year

    # Filter data from 2000 onwards
    df_selected = df_selected[df_selected['Year'] >= 2000]
    df_all = df_all[df_all['Year'] >= 2000]

    # Group data by year and tournament
    df_grouped = df_selected.groupby(['Year', 'Tournament'])['Average'].mean().reset_index()

    # Get unique tournament names
    tournaments = df_grouped['Tournament'].unique()

    # Generate color mapping using Prism color palette
    prism_colors = px.colors.qualitative.Prism
    index_order = custom_index_order(len(tournaments))
    color_map = {
        tournaments[i]: prism_colors[index_order[i] % len(prism_colors)]
        for i in range(len(tournaments))
    }

    # Create plot
    fig = go.Figure()

    # Add a trace for each selected tournament
    for tournament in selected_tournaments:
        df_tournament = df_grouped[df_grouped['Tournament'] == tournament]

        fig.add_trace(go.Scatter(
            x=df_tournament['Year'],
            y=df_tournament['Average'],
            mode='lines',
            name=tournament,
            line=dict(color=color_map.get(tournament, "gray")),
            hovertemplate='%{y}<extra></extra>'
        ))

    # Add a line for the average of all selected or TV tournaments
    if apply_all:
        df_filtered = df_all
        name = "Average of all TV tournaments"
    else:
        df_filtered = df_selected[
            df_selected["Tournament"].isin(selected_tournaments)
        ]
        name = "Average of all selected tournaments"

    avg_all_majors = df_filtered.groupby('Year')['Average'].mean()
    fig.add_trace(go.Scatter(
        x=avg_all_majors.index,
        y=avg_all_majors.values,
        mode='lines',
        line=dict(width=3, dash='dot', color="black"),
        name=name,
        hovertemplate='%{y}<extra></extra>'
    ))

    # Add a regression line if enabled
    if add_regression:
        x_years = avg_all_majors.index.to_numpy()
        y_avg = avg_all_majors.values

        coeffs = np.polyfit(x_years, y_avg, deg=1)
        regression_line = np.poly1d(coeffs)

        fig.add_trace(go.Scatter(
            x=x_years,
            y=regression_line(x_years),
            mode="lines",
            line=dict(color="magenta", width=2, dash="dash"),
            name="Regression Line",
        hovertemplate='%{y}<extra></extra>'
        ))

    # Add standard deviation if enabled
    if add_std:
        min_year = avg_all_majors.index.min()
        std_per_year = df_cleaned[
            df_cleaned['Year'] >= min_year
        ].groupby('Year')['Average'].std()

        fig.add_trace(go.Scatter(
            x=std_per_year.index.tolist() + std_per_year.index[::-1].tolist(),
            y=(avg_all_majors + std_per_year).tolist() +
              (avg_all_majors - std_per_year).tolist()[::-1],
            fill="toself",
            fillcolor="rgba(0, 0, 255, 0.2)",
            line=dict(color="rgba(255,255,255,0)"),
            name="Standard Deviation",
            hoverinfo='skip'
        ))

    # Update layout with English labels
    fig.update_layout(
        title="Development of Average Scores over time",
        xaxis_title="Year",
        yaxis_title="Average Score",
        legend_title="Tournaments",
        hovermode="x unified"
    )

    return fig

# plot_winning_averages(["World Championship"], True, True).show()