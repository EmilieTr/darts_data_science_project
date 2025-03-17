import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_data = "./Data/question 4/question4_doubles.csv"

# CSV-Daten einlesen
df = pd.read_csv(csv_data)

# Line-Chart erstellen
plt.figure(figsize=(10, 6))

# Ein Farbschema festlegen
colors = plt.cm.get_cmap("Paired", len(df["Double"].unique()))  # Nutze "tab10", "viridis" oder andere

# Speichert Legenden-Einträge
legend_entries = []

# Für jedes Doppelfeld eine Linie mit einer spezifischen Farbe erstellen
for i, double_value in enumerate(df["Double"].unique()):
    player_data = df[df["Double"] == double_value]
    player_data = player_data[player_data["Hit"] >= 100]
    color = colors(i)  # Farbe aus dem Farbschema auswählen
    line, = plt.plot(player_data["Year"], player_data["Hit"], label=f'Hit: {double_value}', color=color)
    
    # Speichert den Legenden-Eintrag mit passender Farbe
    legend_entries.append((line, f'Doppelfeld {double_value}'))

# Diagramm-Anpassungen
plt.xlabel('Jahr')
plt.ylabel('Hit-Wert')
plt.title('Entwicklung der Hit-Werte über die Jahre')

# Legende manuell mit den gespeicherten Farben setzen
plt.legend([entry[0] for entry in legend_entries], [entry[1] for entry in legend_entries], title="Doppelfeld", loc="best")

plt.show()
