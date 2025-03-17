import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_distribution_double_fields():
    # CSV-Daten einlesen
    csv_data = "./Data/question 4/question4_doubles.csv"
    df = pd.read_csv(csv_data)

    # Neue Spalte mit der Gesamtanzahl der Würfe pro Spieler
    df["Total"] = df["Hit"] + df["Single"] + df["Outside"] + df["Other"]

    # Bestes Doppelfeld für jeden Spieler ermitteln
    df_max = df.loc[df.groupby("Player")["Total"].idxmax(), ["Player", "Double", "Hit"]]

    # Häufigkeit der Doppelfelder zählen
    double_counts = df_max["Double"].value_counts()

    # Werte unter 1.5% als "Others" zusammenfassen
    total_count = double_counts.sum()
    double_counts_filtered = double_counts[double_counts / total_count >= 0.015]
    other_count = double_counts[double_counts / total_count < 0.015].sum()

    if other_count > 0:
        double_counts_filtered["Others"] = other_count

    # Treffer (Hits) für diese Doppelfelder zählen
    double_counts_hits = df_max.groupby("Double")["Hit"].sum().sort_values(ascending=False)

    # Werte unter 1.5% als "Others" zusammenfassen
    total_hits = double_counts_hits.sum()
    double_counts_hits_filtered = double_counts_hits[double_counts_hits / total_hits >= 0.015]
    other_hits = double_counts_hits[double_counts_hits / total_hits < 0.015].sum()

    if other_hits > 0:
        double_counts_hits_filtered["Others"] = other_hits

    # **Kombinierte Figure mit Subplots**
    fig = make_subplots(
        rows=1, cols=2,  # Zwei Diagramme nebeneinander
        subplot_titles=["Throws on Double Fields", "Hits on Double Fields"],
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )

    # Pie Chart für die Würfe auf die Doppelfelder (linke Seite)
    fig.add_trace(
        go.Pie(
            labels=[f"D {x}" if x != "Others" else x for x in double_counts_filtered.index],
            values=double_counts_filtered.values,
            hole=0.3,
            name="Throws"
        ),
        row=1, col=1
    )

    # Pie Chart für die Treffer auf die Doppelfelder (rechte Seite)
    fig.add_trace(
        go.Pie(
            labels=[f"D {x}" if x != "Others" else x for x in double_counts_hits_filtered.index],
            values=double_counts_hits_filtered.values,
            hole=0.3,
            name="Hits"
        ),
        row=1, col=2
    )

    # Layout-Optimierung
    fig.update_layout(
        title_text="Distribution of Throws & Hits on Double Fields",
        showlegend=True
    )

    return fig

# Diagramm anzeigen
#fig.show()
