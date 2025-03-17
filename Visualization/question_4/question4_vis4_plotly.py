import pandas as pd
import plotly.graph_objects as go

# CSV-Daten einlesen
csv_data = "./Data/question 4/question4_doubles.csv"
df = pd.read_csv(csv_data)

# Spieler S filtern (Ersetze 'Spieler S' mit dem tatsächlichen Namen)
spieler_name = "Michael van Gerwen"
df_spieler = df[df["Player"] == spieler_name]

# Filter: Nur Werte >= 20 behalten
df_spieler = df_spieler[df_spieler["Hit"] >= 20]

# Total Hits
df_spieler["Total"] = df_spieler["Hit"] + df_spieler["Single"] + df_spieler["Outside"] + df_spieler["Other"]

# Berechnung der Doppelquote
df_spieler["Double quota"] = df_spieler["Hit"] / (df_spieler["Hit"] + df_spieler["Single"] + df_spieler["Outside"] + df_spieler["Other"])

# Schritt 1: Berechne den Durchschnitt der Hits pro Doppelfeld
mean_hits = df_spieler.groupby("Double")["Hit"].mean()

# Schritt 2: Filtere nur Doppelfelder mit einem Durchschnitt von >= 120 Hits
top_doppelfelder = mean_hits[mean_hits >= 120].index  # Liste der relevanten Doppelfelder

# Farben für Doppelfelder zuweisen
colors = px.colors.qualitative.Paired
color_map = {double: colors[i % len(colors)] for i, double in enumerate(sorted(df_spieler["Double"].unique()))}

# Figuren erstellen
fig = make_subplots(rows=1, cols=2, subplot_titles=("Throws on Double Fields", "Double Quota"))

# LINKES DIAGRAMM: Hits über die Jahre (ALLE DOPPELFELDER)
for double_value in sorted(df_spieler["Double"].unique()):
    player_data = df_spieler[df_spieler["Double"] == double_value]
    fig.add_trace(
        go.Scatter(x=player_data["Year"], y=player_data["Total"], mode="lines", name=f'D {double_value}', line=dict(color=color_map[double_value])),
        row=1, col=1
    )

# RECHTES DIAGRAMM: Doppelquote über die Jahre (NUR TOP-DOPPELFELDER)
for double_value in top_doppelfelder:
    player_data = df_spieler[df_spieler["Double"] == double_value]
    fig.add_trace(
        go.Scatter(x=player_data["Year"], y=player_data["Double quota"], mode="lines", name=f'D {double_value}', line=dict(color=color_map[double_value])),
        row=1, col=2
    )

# Layout anpassen
fig.update_layout(
    title=f"Player: {spieler_name}",
    xaxis_title="Year",
    yaxis_title="Number of Throws",
    xaxis2_title="Year",
    yaxis2_title="Double Quota",
    showlegend=True,
    height=600,
    width=1200,
)

# Diagramm anzeigen
fig.show()
