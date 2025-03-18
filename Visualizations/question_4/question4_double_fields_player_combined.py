import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_double_fields_player_combined(player, double):

    # CSV-Daten einlesen
    csv_data = "./Data/question 4/question4_doubles.csv"
    df = pd.read_csv(csv_data)

    # Spieler und Double filtern
    double = int(double[1:])
    df_spieler = df[(df["Player"] == player) & (df["Double"] == double)]

    # Berechnung der Gesamtwürfe (Hit + Single + Outside + Other)
    df_spieler["Total"] = df_spieler["Hit"] + df_spieler["Single"] + df_spieler["Outside"] + df_spieler["Other"]

    # Berechnung der Doppelquote
    df_spieler["Double Quota"] = df_spieler["Hit"] / df_spieler["Total"]

    # Farben aus der Prism-Palette von Plotly Express
    prism_colors = px.colors.qualitative.Prism
    color_throws = prism_colors[0]  # Erste Farbe aus der Prism-Palette
    color_quota = prism_colors[6]   # Vierte Farbe aus der Prism-Palette

    # Interaktive Grafik erstellen
    fig = go.Figure()

    # Linie für Gesamtwürfe (linke y-Achse)
    fig.add_trace(go.Scatter(
        x=df_spieler["Year"], 
        y=df_spieler["Total"], 
        mode="lines+markers", 
        name="Number of Throws",
        yaxis="y1",
        line=dict(color=color_throws)
    ))

    # Linie für Doppelquote (rechte y-Achse)
    fig.add_trace(go.Scatter(
        x=df_spieler["Year"], 
        y=df_spieler["Double Quota"], 
        mode="lines+markers", 
        name="Double Quota",
        yaxis="y2",
        line=dict(color=color_quota, dash="dash")
    ))

    # Layout anpassen
    fig.update_layout(
        title=f"Number of Throws and Double Quota from {player} on D {double}",
        xaxis_title="Year",
        yaxis=dict(
            title="Number of Throws",
            tickfont=dict(color=color_throws)
        ),
        yaxis2=dict(
            title="Double Quota",
            tickfont=dict(color=color_quota),
            overlaying="y",
            side="right"
        ),
        legend=dict(x=0.01, y=0.99),
        height=600,
        width=1000
    )
    
    return fig
