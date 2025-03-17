import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_data = "./Data/question 4/question4_doubles.csv"

# CSV-Daten einlesen
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

# **Schritt 1: Berechne den Durchschnitt der Hits pro Doppelfeld**
mean_hits = df_spieler.groupby("Double")["Hit"].mean()

# **Schritt 2: Filtere nur Doppelfelder mit einem Durchschnitt von >= 100 Hits**
top_doppelfelder = mean_hits[mean_hits >= 120].index  # Liste der relevanten Doppelfelder

# **Schritt 3: Feste Farben für jedes Doppelfeld zuweisen**
all_doubles = sorted(df_spieler["Double"].unique(), key=int)  # Sortierte Liste aller Doppelfelder
color_palette = plt.cm.get_cmap("Paired", len(all_doubles))  # Erstelle Farbpalette
color_map = {double: color_palette(i) for i, double in enumerate(all_doubles)}  # Feste Farbzuteilung

# Subplots erstellen (1 Zeile, 2 Spalten)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Speichert Legenden-Einträge für beide Diagramme
legend_entries_hits = []
legend_entries_quote = []

### LINKES DIAGRAMM: Hits über die Jahre (ALLE DOPPELFELDER) ###
for i, double_value in enumerate(sorted(df_spieler["Double"].unique(), key=int)):  # Sortiere numerisch
    player_data = df_spieler[df_spieler["Double"] == double_value]
    color = color_map[double_value]
    line, = axes[0].plot(player_data["Year"], player_data["Total"], label=f'D {double_value}', color=color)
    legend_entries_hits.append((line, f'D {double_value}'))

axes[0].set_xlabel('Year')
axes[0].set_ylabel('Number of Throws')
axes[0].set_title(f'Throws on Double Fields from {spieler_name}')

# Sortierte Legende für erstes Diagramm
legend_entries_hits.sort(key=lambda x: int(x[1].split()[-1]))
axes[0].legend(
    [entry[0] for entry in legend_entries_hits],  
    [entry[1] for entry in legend_entries_hits],  
    title="Double Field", loc="best"
)

### RECHTES DIAGRAMM: Doppelquote über die Jahre (NUR TOP-DOPPELFELDER) ###
for i, double_value in enumerate(sorted(top_doppelfelder, key=int)):  # Nur gefilterte Doppelfelder
    player_data = df_spieler[df_spieler["Double"] == double_value]
    color = color_map[double_value]
    line, = axes[1].plot(player_data["Year"], player_data["Double quota"], label=f'D {double_value}', color=color)
    legend_entries_quote.append((line, f'D {double_value}'))

axes[1].set_xlabel('Year')
axes[1].set_ylabel('Double Quota')
axes[1].set_title(f'Double Quota from {spieler_name} (only double fields with Ø ≥ 120 Hits)')

# Sortierte Legende für zweites Diagramm
legend_entries_quote.sort(key=lambda x: int(x[1].split()[-1]))
axes[1].legend(
    [entry[0] for entry in legend_entries_quote],  
    [entry[1] for entry in legend_entries_quote],  
    title="Double Field", loc="best"
)

# Layout anpassen & Diagramm anzeigen
plt.tight_layout()
plt.show()


'''import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_data = "./Data/question1_doubles.csv"

# CSV-Daten einlesen
df = pd.read_csv(csv_data)

# Spieler S filtern (Ersetze 'Spieler S' mit dem tatsächlichen Namen)
spieler_name = "Michael van Gerwen"
df_spieler = df[df["Player"] == spieler_name]

# Filter: Nur Werte >= 20 behalten
df_spieler = df_spieler[df_spieler["Hit"] >= 20]

# Berechnung der Doppelquote
df_spieler["Doppelquote"] = df_spieler["Hit"] / (df_spieler["Hit"] + df_spieler["Single"] + df_spieler["Outside"] + df_spieler["Other"])

# Subplots erstellen (1 Zeile, 2 Spalten)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Ein Farbschema für Konsistenz
colors = plt.cm.get_cmap("Paired", len(df_spieler["Double"].unique()))

# Speichert Legenden-Einträge für beide Diagramme
legend_entries_hits = []
legend_entries_quote = []

### LINKES DIAGRAMM: Hits über die Jahre ###
for i, double_value in enumerate(sorted(df_spieler["Double"].unique(), key=int)):  # Sortiere numerisch
    player_data = df_spieler[df_spieler["Double"] == double_value]
    color = colors(i)
    line, = axes[0].plot(player_data["Year"], player_data["Hit"], label=f'Doppelfeld {double_value}', color=color)
    legend_entries_hits.append((line, f'D {double_value}'))

axes[0].set_xlabel('Jahr')
axes[0].set_ylabel('Anzahl Hits')
axes[0].set_title(f'Hits auf Doppelfelder von {spieler_name}')
axes[0].legend(title="Doppelfeld", loc="best")

# Sortiere die Legende nach der Doppelfeldnummer
legend_entries_hits.sort(key=lambda x: int(x[1].split()[-1]))
axes[0].legend(
    [entry[0] for entry in legend_entries_hits],  # Linienobjekte
    [entry[1] for entry in legend_entries_hits],  # Labels
    title="Doppelfeld", loc="best"
)

### RECHTES DIAGRAMM: Doppelquote über die Jahre ###
for i, double_value in enumerate(sorted(df_spieler["Double"].unique(), key=int)):  # Sortiere numerisch
    player_data = df_spieler[df_spieler["Double"] == double_value]
    color = colors(i)
    line, = axes[1].plot(player_data["Year"], player_data["Doppelquote"], label=f'Doppelfeld {double_value}', color=color)
    legend_entries_quote.append((line, f'D {double_value}'))

axes[1].set_xlabel('Jahr')
axes[1].set_ylabel('Doppelquote')
axes[1].set_title(f'Doppelquote von {spieler_name}')

# Sortiere die Legende nach der Doppelfeldnummer
legend_entries_quote.sort(key=lambda x: int(x[1].split()[-1]))
axes[1].legend(
    [entry[0] for entry in legend_entries_quote],  # Linienobjekte
    [entry[1] for entry in legend_entries_quote],  # Labels
    title="Doppelfeld", loc="best"
)

# Layout anpassen & Diagramm anzeigen
plt.tight_layout()
plt.show()
'''