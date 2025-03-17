import pandas as pd
import plotly.graph_objects as go

# CSV-Daten einlesen
csv_data = "./Data/question 4/question4_doubles.csv"
df = pd.read_csv(csv_data)

# Spieler S und Double 20 filtern
spieler_name = "Michael van Gerwen"
double_value = 20
df_spieler = df[(df["Player"] == spieler_name) & (df["Double"] == double_value)]

# Berechnung der Gesamtwürfe (Hit + Single + Outside + Other)
df_spieler["Total"] = df_spieler["Hit"] + df_spieler["Single"] + df_spieler["Outside"] + df_spieler["Other"]

# Berechnung der Doppelquote
df_spieler["Double Quota"] = df_spieler["Hit"] / df_spieler["Total"]

# Interaktive Grafik erstellen
fig = go.Figure()

# Linie für Gesamtwürfe (linke y-Achse)
fig.add_trace(go.Scatter(
    x=df_spieler["Year"], 
    y=df_spieler["Total"], 
    mode="lines+markers", 
    name="Number of Throws",
    yaxis="y1",
    line=dict(color="blue")
))

# Linie für Doppelquote (rechte y-Achse)
fig.add_trace(go.Scatter(
    x=df_spieler["Year"], 
    y=df_spieler["Double Quota"], 
    mode="lines+markers", 
    name="Double Quota",
    yaxis="y2",
    line=dict(color="red", dash="dash")
))

# Layout anpassen
fig.update_layout(
    title=f"Number of Throws and Double Quota from {spieler_name} on D {double_value}",
    xaxis_title="Year",
    yaxis=dict(
        title="Number of Throws",
        titlefont=dict(color="blue"),
        tickfont=dict(color="blue")
    ),
    yaxis2=dict(
        title="Double Quota",
        titlefont=dict(color="red"),
        tickfont=dict(color="red"),
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0.01, y=0.99),
    height=600,
    width=1000
)

# Diagramm anzeigen
fig.show()
