import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def plot_average_line_chart(ranking_position, list_of_years):
    """
    Create a line chart showing player averages across specified years.
    """
    def convert_name(name):
        """
        Convert names from 'SURNAME, First_name' to 'First_name Surname' format.
        """
        if ", " in name:
            surname, first_name = name.split(", ", 1)
            surname = surname.capitalize()
            return f"{first_name} {surname}"
        return name


    # Load averages
    file_averages = 'Data/Darts_Orakel_Stats/Averages.csv'
    df_averages = pd.read_csv(file_averages)

    # Convert Stat to float
    df_averages['Stat'] = df_averages['Stat'].astype(float)

    # Convert years from string to integer
    list_of_years = [int(i) for i in list_of_years]

    # Construct data frame with rank, player and average
    data_frames = []
    for year in list_of_years:
        file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'

        df = pd.read_csv(file)
        list = [
            convert_name(name) for name in df['Name'].head(ranking_position)
        ]

        ranks = []
        players = []
        averages = []

        for rank, player in enumerate(list, start=1):
            # Extract player data for specific year
            average_row = df_averages[
                (df_averages['Player'] == player) & 
                (df_averages['Year'] == year)
            ]
            
            if not average_row.empty:
                # If average for year was found, save average
                averages.append(average_row['Stat'].values[0])
            else:
                # If no average for year was found, save None
                averages.append(None)
            
            ranks.append(rank)
            players.append(player)
        
        # Create data frame from the year
        df_averages_new = pd.DataFrame({
            'Rank': ranks,
            'Player': players,
            'Stat': averages,
            'Year': year
        })
        data_frames.append(df_averages_new)
    

    # Combine both datasets
    df_combined = pd.concat(data_frames)

    # Get Prism colors
    colors = px.colors.qualitative.Prism
    for color in px.colors.qualitative.Safe:
        colors.append(color)
    del colors[9]
    del colors[10]

    # Create figure
    fig = go.Figure()

    # Add lines for each year
    for year, color in zip(list_of_years, colors):
        subset = df_combined[df_combined["Year"] == year]
        
        fig.add_trace(go.Scatter(
            x=subset["Rank"],  # order of merit rank on x-axis
            y=subset["Stat"],  # averages on y-axis
            mode='lines',  
            name=str(year),  # Name for the legend (year)
            line=dict(color=color, width=2),
            marker=dict(size=6, symbol='circle', opacity=1),
            text=subset["Player"],
            hovertemplate=(
                'Rank: %{x}<br>Average: %{y}<br>Player: %{text}'
            ),
            connectgaps=True
        ))

    # If there's only one line, ensure the legend is displayed
    if len(list_of_years) == 1:
        fig.add_trace(go.Scatter(
            x=[None],  # Invisible line for legend
            y=[None],
            mode='lines',
            name='',  # empty name for the legend
            line=dict(color='rgba(0,0,0,0)', width=0),  # Invisible line
            hoverinfo='skip'  # Skip hover
        ))

    # Set layout
    fig.update_layout(
        title="Development of Averages by Order of Merit Rank",
        xaxis_title="Order of Merit Rank",
        yaxis_title="Average",
        xaxis=dict(tickmode='linear', dtick=1), 
        legend_title="Year",  # Title of the legend
        legend=dict(
            title="Year",
            x=1.1,  # Position of the legend (from 0 to 1, relative to chart)
            y=0.95,  # Y position of the legend
            traceorder="normal",  # Determines the order of items in the legend
            font=dict(size=12),  # Font size of legend
        )
    )

    return fig


