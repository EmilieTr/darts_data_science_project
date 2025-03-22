import pandas as pd
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats

def plot_histogram(selected_tournaments):
    # CSV-Datei laden
    file = 'Data/question 2/question2.csv'
    df = pd.read_csv(file)
    
    # Spalten bereinigen
    df.columns = df.columns.str.strip()

    # Daten filtern (nur relevante Turniere und gültige Averages)
    df_cleaned = df.dropna(subset=['Average'])
    df_cleaned = df_cleaned[df_cleaned['Average'] >= 10]
    df_selected = df_cleaned[df_cleaned['Tournament'].isin(selected_tournaments)]

    # Werte für die Normalverteilung berechnen
    mu, sigma = df_selected['Average'].mean(), df_selected['Average'].std()

    # Erstellen eines Histogramms
    hist_data = np.histogram(df_selected['Average'], bins=20)
    bin_edges = hist_data[1]
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2  # Mittlere Werte der Bins

    # Normalverteilungskurve generieren
    x_values = np.linspace(min(df_selected['Average']), max(df_selected['Average']), 100)
    y_values = stats.norm.pdf(x_values, mu, sigma) * len(df_selected) * (bin_edges[1] - bin_edges[0])

    # Erstellen der Plotly-Figur
    fig = go.Figure()

    # Histogramm hinzufügen
    fig.add_trace(go.Bar(
        x=bin_centers, 
        y=hist_data[0], 
        name="Histogram", 
        marker=dict(color='lightblue', opacity=0.7),
    ))

    # Normalverteilungskurve hinzufügen
    fig.add_trace(go.Scatter(
        x=x_values, 
        y=y_values, 
        mode="lines", 
        line=dict(color="red", width=2), 
        name="Normal Distribution"
    ))

    # Layout anpassen
    fig.update_layout(
        title="Distribution of Winning Averages",
        xaxis_title="Average Score",
        yaxis_title="Frequency",
        legend_title="Legend",
        hovermode="x unified"
    )

    return fig
