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
    prism_colors = px.colors.qualitative.Prism
    colors = []

    # Set colors
    counter = 0
    for i in range(len(list_of_years)):
        if counter == 11:
            counter = 0
        colors.append(prism_colors[counter])
        counter += 1

    # Create figure
    fig = go.Figure()

    # Add lines for each year
    for year, color in zip(list_of_years, colors):
        subset = df_combined[df_combined["Year"] == year]
        
        fig.add_trace(go.Scatter(
            x=subset["Rank"],  # order of merit rank on x-axis
            y=subset["Stat"],  # averages on y-axis
            mode='lines',  
            name=str(year),  
            line=dict(color=color, width=2),
            marker=dict(size=6, symbol='circle', opacity=1),
            text=subset["Player"],
            hovertemplate=(
                'Rank: %{x}<br>Average: %{y}<br>Player: %{text}'
            ),
            connectgaps=True
        ))

    # Set layout
    fig.update_layout(
        title="Development of Averages by Order of Merit Rank",
        xaxis_title="Order of Merit Rank",
        yaxis_title="Average",
        xaxis=dict(tickmode='linear', dtick=1), 
        legend_title="Year"
    )

    return fig

# Show Plot
# all_years = list(range(2009, 2025))
# years = [2009, 2024]
# fig = plot_average_line_chart(50, years)
# fig.show()

