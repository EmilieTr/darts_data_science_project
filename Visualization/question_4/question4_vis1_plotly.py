import pandas as pd
import plotly.graph_objects as go

# CSV-Daten einlesen
csv_data = "./Data/question 4/question4_doubles.csv"
df = pd.read_csv(csv_data, header=0)

# Berechnung der verfehlten Würfe
df["Miss"] = df["Single"] + df["Outside"] + df["Other"]

# Daten aggregieren nach Doppelfeld
df_agg = df.groupby("Double")[["Miss", "Hit"]].sum().reset_index()

# Stacked Bar Chart mit Plotly erstellen
fig = go.Figure()

# "Hit"-Balken hinzufügen
fig.add_trace(go.Bar(
    x=df_agg["Double"],
    y=df_agg["Hit"],
    name="Hit",
    marker_color="blue"
))

# "Miss"-Balken auf die "Hit"-Balken stapeln
fig.add_trace(go.Bar(
    x=df_agg["Double"],
    y=df_agg["Miss"],
    name="Miss",
    marker_color="red"
))

# Layout anpassen
fig.update_layout(
    barmode="stack",
    title="Stacked Bar Chart of Hits and Misses per Double Field",
    xaxis_title="Double Fields",
    yaxis_title="Number of Throws",
    xaxis=dict(type="category"),  # X-Achse als kategoriale Werte (für bessere Darstellung)
    legend_title="Outcome"
)

# Diagramm anzeigen
fig.show()
