import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def plot_distribution_double_fields():
    # CSV-Daten einlesen
    csv_data = "./Data/question 4/question4_doubles.csv"
    df = pd.read_csv(csv_data)

    # Erstelle eine neue Spalte mit der Gesamtzahl der Würfe pro Spieler
    df["Total"] = df["Hit"] + df["Single"] + df["Outside"] + df["Other"]

    # Bestimme das beste Doppelfeld für jeden Spieler (basierend auf der Gesamtzahl der Würfe)
    df_max = df.loc[df.groupby("Double")["Total"].idxmax(), ["Double", "Hit"]]

    # Zähle die Häufigkeit jedes Doppelfeldes
    double_counts = df["Double"].value_counts()

    # Werte unter 1,5% als "Others" gruppieren
    total_count = double_counts.sum()
    double_counts_filtered = double_counts[double_counts / total_count >= 0.015]
    other_count = double_counts[double_counts / total_count < 0.015].sum()

    if other_count > 0:
        double_counts_filtered["Others"] = other_count

    # Zähle die Hits für jedes Doppelfeld
    double_counts_hits = df_max.groupby("Double")["Hit"].sum().sort_values(ascending=False)

    # Werte unter 1,5% als "Others" gruppieren
    total_hits = double_counts_hits.sum()
    double_counts_hits_filtered = double_counts_hits[double_counts_hits / total_hits >= 0.015]
    other_hits = double_counts_hits[double_counts_hits / total_hits < 0.015].sum()

    if other_hits > 0:
        double_counts_hits_filtered["Others"] = other_hits

    # Farben aus der Prism-Farbpalette für jedes Doppelfeld
    prism_colors = px.colors.qualitative.Prism
    color_map = {double: prism_colors[i % len(prism_colors)] for i, double in enumerate(double_counts_filtered.index)}

    # Sortiere die "Double"-Feld-Indizes nach der Zahl nach "D"
    double_counts_filtered = double_counts_filtered.sort_index(ascending=True, 
        key=lambda x: x.str.extract('(\d+)').astype(float).fillna(0).astype(int).squeeze())
    double_counts_hits_filtered = double_counts_hits_filtered.sort_index(ascending=True, 
        key=lambda x: x.str.extract('(\d+)').astype(float).fillna(0).astype(int).squeeze())

    # Wenn "Others" vorhanden ist, wird es ans Ende verschoben
    if 'Others' in double_counts_filtered.index:
        others_value = double_counts_filtered.pop('Others')
        double_counts_filtered['Others'] = others_value

    if 'Others' in double_counts_hits_filtered.index:
        others_value = double_counts_hits_filtered.pop('Others')
        double_counts_hits_filtered['Others'] = others_value

    # Erstelle das Diagramm mit zwei Subplots
    fig = make_subplots(
        rows=1, cols=2,  # Zwei Diagramme nebeneinander
        subplot_titles=["Throws on Double Fields", "Hits on Double Fields"],
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )

    # Pie Chart für die Anzahl der Würfe auf den Doppelfeldern (linke Seite)
    fig.add_trace(
        go.Pie(
            labels=[f"D {x}" if x != "Others" else x for x in double_counts_filtered.index],
            values=double_counts_filtered.values,
            hole=0.3,
            name="Throws",
            marker=dict(colors=[color_map.get(x, "gray") for x in double_counts_filtered.index])  # Dynamische Farbzuteilung
        ),
        row=1, col=1
    )

    # Pie Chart für Hits auf den Doppelfeldern (rechte Seite)
    fig.add_trace(
        go.Pie(
            labels=[f"D {x}" if x != "Others" else x for x in double_counts_hits_filtered.index],
            values=double_counts_hits_filtered.values,
            hole=0.3,
            name="Hits",
            marker=dict(colors=[color_map.get(x, "gray") for x in double_counts_hits_filtered.index])  # Dynamische Farbzuteilung
        ),
        row=1, col=2
    )

    # Layout-Optimierung
    fig.update_layout(
        title_text="Distribution of Throws & Hits on Double Fields",
        showlegend=True
    )

    return fig
