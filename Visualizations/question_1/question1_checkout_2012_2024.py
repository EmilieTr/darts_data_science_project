import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

def plot_checkout_2012_2024(ranking_position):
    """
    Plot checkout percentages for top players in 2012 and 2024.
    """
    def convert_name(name):
        """
        Convert names from 'SURNAME, First_name' to 'First_name Surname' format."
        """
        if ", " in name:
            surname, first_name = name.split(", ", 1)
            surname = surname.capitalize()
            return f"{first_name} {surname}"
        return name 

    # Load CSV files
    file_2012 = 'Data/order_of_merit/order_of_merit_year_2012.csv'
    file_2024 = 'Data/order_of_merit/order_of_merit_year_2024.csv'
    df_2012 = pd.read_csv(file_2012)
    df_2024 = pd.read_csv(file_2024)

    # Convert player names
    list_2012 = [
        convert_name(name) for name in df_2012['Name'].head(ranking_position)
    ]
    list_2024 = [
        convert_name(name) for name in df_2024['Name'].head(ranking_position)
    ]

    # Load check out percentages
    file_averages = 'Data/Darts_Orakel_Stats/Checkout Pcnt.csv'
    df_averages = pd.read_csv(file_averages)

    # Convert Stat to float
    df_averages['Stat'] = (
        df_averages['Stat'].str.rstrip('%').astype(float) / 100
    )

    # Extract data for 2012 and 2024
    df_averages_2012 = df_averages[
        (df_averages['Year'] == 2012) & (df_averages['Player'].isin(list_2012))
    ]
    df_averages_2024 = df_averages[
        (df_averages['Year'] == 2024) & (df_averages['Player'].isin(list_2024))
    ]

    # Add Year column
    df_averages_2012['Year'] = 2012
    df_averages_2024['Year'] = 2024

    # Combine both datasets
    df_combined = pd.concat([df_averages_2012, df_averages_2024])

    # Create X positions for bars
    players = df_combined["Player"].unique()
    x_indexes = np.arange(len(players))
    width = 0.4

    # Get Prism colors for the bars
    prism_colors = px.colors.qualitative.Prism
    color_2012 = prism_colors[0]
    color_2024 = prism_colors[6]

    # Create figure
    fig = go.Figure()

    # Add bars for each year
    for i, year in enumerate([2012, 2024]):
        subset = df_combined[df_combined["Year"] == year]
        player_positions = [
            players.tolist().index(player) for player in subset["Player"]
        ]
        
        # Use the colors from Prism for each year
        bar_color = color_2012 if year == 2012 else color_2024
        
        fig.add_trace(go.Bar(
            x=[players[pos] for pos in player_positions],
            y=subset["Stat"],
            name=str(year),
            offset=i * width - width / 2,
            marker=dict(color=bar_color)
        ))

    # Update layout
    fig.update_layout(
        title="Development of Averages over the Years",
        xaxis_title="Players",
        yaxis_title="Average",
        barmode='group',
        xaxis=dict(tickangle=-45),
        legend_title="Year"
    )
    
    return fig

# Show Plot
# fig = plot_checkout_2012_2024(50)
# fig.show()
