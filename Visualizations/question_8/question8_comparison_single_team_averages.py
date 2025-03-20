import pandas as pd
import plotly.graph_objects as go
import pycountry
import plotly.express as px
import numpy as np
import streamlit as st

def plot_comparison_single_team_averages():

    def get_country_code(country_name):
        ioc_mapping = {
            "DEU": "GER",  # Germany
            "CHE": "SUI",  # Switzerland
            "GRC": "GRE",
            "KOR": "KOR",  # South Korea
            "PRK": "PRK",  # North Korea
            "ZAF": "RSA",  # South Africa
            "IRN": "IRI",
            "NLD": "NED"
        }

        countries_not_in_iso = {
            "England": "ENG",
            "Scotland": "SCO",
            "Wales": "WAL",
            "Northern Ireland": "NIR",
            "Russia": "RUS",
            "Chinese Taipei": "CHI",
            "Netherlands": "NED"
        }

        try:
            country = pycountry.countries.get(name=country_name)
            if country_name in countries_not_in_iso:
                return countries_not_in_iso[country_name]
            if country.alpha_3 in ioc_mapping:
                return ioc_mapping[country.alpha_3]
            return country.alpha_3  # Standard-3-Buchstaben-Kürzel
        except AttributeError:
            return None  # Falls das Land nicht gefunden wird

    # CSV-Dateien einlesen
    player_data = pd.read_csv('./Data/Darts_Orakel_Stats/Averages.csv')
    country_data = pd.read_csv('./Data/Darts_Orakel_Stats/world_cup_Averages.csv')

    # DataFrames für Spieler und Länder erstellen
    players_df = country_data[country_data['Country'].notna()]  # Nur Spieler
    countries_df = country_data[country_data['Country'].isna()]  # Nur Länder

    # Anwendung der Funktion auf die 'Country'-Spalte und Erstellung einer neuen 'Country_Code'-Spalte
    countries_df['Country'] = countries_df['Player'].apply(get_country_code)

    # Spieler aus der ersten CSV, die auch in der zweiten CSV vorkommen
    players_in_both = player_data[player_data['Player'].isin(players_df['Player'])]

    # Überprüfen, ob Spieler vorhanden sind
    print(f"Anzahl Spieler, die in beiden DataFrames vorkommen: {len(players_in_both)}")

    # Merge der beiden DataFrames basierend auf Jahr und Land
    merged_df = pd.merge(players_in_both, countries_df, on=['Country', 'Year'], suffixes=('_player', '_country'))

    # Überprüfen, ob der Merge funktioniert hat
    print(f"Anzahl der Zeilen im zusammengeführten DataFrame: {len(merged_df)}")

    # Prozentwerte in numerische Werte umwandeln
    merged_df['Stat_player'] = merged_df['Stat_player'].str.replace('%', '').astype(float)
    merged_df['Stat_country'] = merged_df['Stat_country'].str.replace('%', '').astype(float)

    # Berechnung der Differenz    
    merged_df['Deviation'] = merged_df['Stat_country'] - merged_df['Stat_player']

    # Zählen der besseren und schlechteren Abweichungen für jedes Land
    comparison_counts = merged_df.groupby('Country').agg(
        better_count=('Deviation', lambda x: x[x > 0].sum()),  # Positive Abweichungen aufsummieren
        worse_count=('Deviation', lambda x: -x[x < 0].sum())  # Negative Abweichungen aufsummieren
    ).reset_index()

    # 📊 INTERAKTIVES BALKENDIAGRAMM ERSTELLEN
    fig = go.Figure()

    # Positive Balken (bessere Spieler) mit Prism-Palette-Farben
    prism_colors = px.colors.qualitative.Prism
    fig.add_trace(go.Bar(
        x=comparison_counts['Country'],
        y=comparison_counts['better_count'],
        name="Player better than team",
        marker_color=prism_colors[0],  # Verwenden der ersten Farbe in der Prism-Palette
        hovertemplate="%{y} players better<extra></extra>"
    ))

    # Negative Balken (schlechtere Spieler) mit Prism-Palette-Farben
    fig.add_trace(go.Bar(
        x=comparison_counts['Country'],
        y=-comparison_counts['worse_count'],  # Negativer Wert für visuelle Unterscheidung
        name="Player worse than team",
        marker_color=prism_colors[6],  # Verwenden der siebten Farbe in der Prism-Palette
        hovertemplate="%{y} players worse<extra></extra>"
    ))

    # Layout anpassen
    fig.update_layout(
        title="Comparison: Player's Checkout vs. Team Checkout (World Cup)",
        xaxis_title="Country",
        yaxis_title="Number of Players (Summed over Years)",
        barmode="relative",  # Balken auf der gleichen Achse (positive & negative Werte)
        template="plotly_white",
        showlegend=True,
        height=600,
        width=1000
    )

    return fig

# Diagramm anzeigen
#fig.show()

# Funktion ausführen
#plot_comparison_single_team()
