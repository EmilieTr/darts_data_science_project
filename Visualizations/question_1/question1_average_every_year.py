import pandas as pd
import plotly.graph_objects as go
import numpy as np

def plot_average_every_year():

    # Function to convert names from format "SURNAME, First_name" into "First_name Surname"
    def convert_name(name):
        if ", " in name:
            surname, first_name = name.split(", ", 1)  # Divide surname and first name
            surname = surname.capitalize()  # Only the first letter of surname is capitalized
            return f"{first_name} {surname}"
        return name 

    # Load averages
    file_averages = 'Data/Darts_Orakel_Stats/Averages.csv'
    df_averages = pd.read_csv(file_averages)

    averages_stat = {}
    for year in range(2009, 2025):
        sum = 0
        count = 0

        file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'
        df = pd.read_csv(file)

        list_best_players = [convert_name(name) for name in df['Name'].head(10)]
        df_averages_year = df_averages[(df_averages['Year'] == year) & (df_averages['Player'].isin(list_best_players))]
        
        if not df_averages_year.empty:
            df_averages_year['Stat'] = df_averages_year['Stat'].astype(float)
            for val in df_averages_year['Stat']:
                sum += val
                count += 1
            sum = round((sum / count))
            averages_stat[year] = sum

    # create bar chart 
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(averages_stat.keys()),  # Jahre auf der X-Achse
        y=list(averages_stat.values()),  # Durchschnittliche Checkout-Quote auf der Y-Achse
        text=[f"{v:.1f}" for v in averages_stat.values()],  # Prozentwerte als Text
        textposition='outside',  # Text über den Balken platzieren
        marker_color='royalblue'  # Farbe der Balken
    ))

    # Layout anpassen
    fig.update_layout(
        title="Average per year",
        xaxis_title="Jahr",
        yaxis_title="Average",
        yaxis_tickformat=".",  # Y-Achse als Prozentwerte anzeigen
        template="plotly_white"
    )
    return fig



# Diagramm anzeigen
fig = plot_average_every_year()
#fig.show()