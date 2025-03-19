import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def plot_average_2009_2024(ranking_position, list_of_years):
    # Function to convert names from format "SURNAME, First_name" into "First_name Surname"
    def convert_name(name):
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

    
    

    data_frames = []
    for year in list_of_years:
        file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'

        df = pd.read_csv(file)
        list = [convert_name(name) for name in df['Name'].head(ranking_position)]
        # Leere Listen für die Rangfolge, Spieler und Averages
        ranks = []
        players = []
        averages = []

        for rank, player in enumerate(list, start=1):
            # Überprüfen, ob der Spieler im DataFrame der Averages ist und das Jahr 2009 entspricht
            
            average_row = df_averages[(df_averages['Player'] == player) & (df_averages['Year'] == year)]
            
            if not average_row.empty:
                # Wenn ein Average für das Jahr 2009 gefunden wurde, füge es zur Liste hinzu
                averages.append(average_row['Stat'].values[0])
            else:
                # Wenn kein Average für das Jahr 2009 gefunden wurde, füge `None` hinzu
                averages.append(None)
            
            # Füge Rang und Spieler zur Liste hinzu
            ranks.append(rank)
            players.append(player)
        
        # Erstelle das DataFrame aus den gesammelten Daten
        df_averages_new = pd.DataFrame({
            'Rank': ranks,
            'Player': players,
            'Stat': averages,
            'Year': year
        })
        data_frames.append(df_averages_new)
    

    # Combine both datasets
    df_combined = pd.concat(data_frames)
    print(df_combined)
    # Get Prism colors for the lines
    prism_colors = px.colors.qualitative.Prism
    colors = []
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
        
        # Erstelle Scatter-Plot mit connectgaps=True, um die Linie fortzusetzen, auch wenn NaN-Werte vorhanden sind
        fig.add_trace(go.Scatter(
            x=subset["Rank"],  # Order of Merit rank auf der x-Achse
            y=subset["Stat"],  # Averages auf der y-Achse
            mode='lines+markers',  # Linien-Diagramm mit Markern
            name=str(year),  # Legendenname
            line=dict(color=color, width=2),
            marker=dict(size=6, symbol='circle', opacity=1),
            text=subset["Player"],  # Spielername als Hover-Text
            hovertemplate='Rank: %{x}<br>Average: %{y}<br>Player: %{text}',
            connectgaps=True  # Setzt die Linie fort, auch wenn NaN-Werte in den Daten vorhanden sind
        ))

    # Update layout
    fig.update_layout(
        title="Development of Averages by Order of Merit Rank",
        xaxis_title="Order of Merit Rank",
        yaxis_title="Average",
        xaxis=dict(tickmode='linear', dtick=1),  # Show all ranks from 1 to ranking_position
        legend_title="Year"
    )

    return fig

# Show Plot
'''all = []
for year in range(2009, 2025):
    all.append(year)
years = [2009,2024]
fig = plot_average_2009_2024(50, years)
#fig = plot_average_2009_2024(50, all)
fig.show()'''

