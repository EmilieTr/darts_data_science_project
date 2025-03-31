import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def plot_checkout_line_chart(ranking_position, list_of_years):
    """
    Create a line chart showing player checkout percentages across years."
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


    # Load checkout percentages
    file_checkout = 'Data/Darts_Orakel_Stats/player_checkout.csv'
    df_checkout = pd.read_csv(file_checkout)

    # Convert Stat to float
    df_checkout['Stat'] = (
        df_checkout['Stat'].str.rstrip('%').astype(float) / 100
    )

    # Convert years from string to integer
    list_of_years = [int(i) for i in list_of_years]
    
    # Construct data frame with rank, player and checkout percentages
    data_frames = []
    for year in list_of_years:
        file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'

        df = pd.read_csv(file)
        list = [
            convert_name(name) 
            for name in df['Name'].head(ranking_position)
        ]

        ranks = []
        players = []
        checkout_quote = []

        for rank, player in enumerate(list, start=1):
            # Extract player in specific year
            checkout_row = df_checkout[
                (df_checkout['Player'] == player) & 
                (df_checkout['Year'] == year)
            ]
            
            if not checkout_row.empty:
                # If checkout quote for year was found, save average
                checkout_quote.append(checkout_row['Stat'].values[0])
            else:
                # If no checkout quote for year was found, save None
                checkout_quote.append(None)
            
            ranks.append(rank)
            players.append(player)
        
        # Create data frame out of collected data
        df_averages_new = pd.DataFrame({
            'Rank': ranks,
            'Player': players,
            'Stat': checkout_quote,
            'Year': year
        })
        data_frames.append(df_averages_new)
    

    # Combine both datasets
    df_combined = pd.concat(data_frames)

    # Get Prism colors for the lines
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
            x=subset["Rank"],
            y=subset["Stat"],
            mode='lines',  
            name=str(year),  
            line=dict(color=color, width=2),
            marker=dict(size=6, symbol='circle', opacity=1),
            text=subset["Player"],  
            hovertemplate=(
                'Rank: %{x}<br>'
                'Checkout Percentage: %{y:.1%}<br>'
                'Player: %{text}'
            ),
            connectgaps=True
        ))

    # If there's only one line, ensure the legend is displayed
    if len(list_of_years) == 1:
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            name='',  # empty name for the legend
            line=dict(color='rgba(0,0,0,0)', width=0),
            hoverinfo='skip'  # Skip hover
        ))

    # Set layout
    fig.update_layout(
        title="Development of Checkout Percentages by Order of Merit Rank",
        xaxis_title="Order of Merit Rank",
        yaxis_title="Checkout Percentage (%)",
        yaxis_tickformat=".0%",
        xaxis=dict(tickmode='linear', dtick=1),  
        legend_title="Year",
        legend=dict(
            title="Year",
            x=1.1,
            y=0.95,
            traceorder="normal",
            font=dict(size=12),
        )
    )

    return fig

# Show Plot
# all = []
# for year in range(2012, 2025):
#     all.append(year)
# years = [2012,2024]
# fig = plot_average_2009_2024(50, years)
# fig = plot_average_2009_2024(50, all)
# fig.show()