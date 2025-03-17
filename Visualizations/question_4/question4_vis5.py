import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_data = "./Data/question 4/question4_doubles.csv"

# CSV-Daten einlesen
df = pd.read_csv(csv_data)

# Spieler S und Double 20 filtern
spieler_name = "Michael van Gerwen"
double_value = 20
df_spieler = df[(df["Player"] == spieler_name) & (df["Double"] == double_value)]

# Berechnung der Gesamtwürfe (Hit + Single + Outside + Other)
df_spieler["Total"] = df_spieler["Hit"] + df_spieler["Single"] + df_spieler["Outside"] + df_spieler["Other"]

# Berechnung der Doppelquote
df_spieler["Double Quota"] = df_spieler["Hit"] / df_spieler["Total"]

# Colors
colors = plt.get_cmap("Paired")(np.linspace(0, 1, 2))

# **Diagramm mit zwei y-Achsen erstellen**
fig, ax1 = plt.subplots(figsize=(10, 6))

# **Linie für Gesamtwürfe (linke y-Achse)**
#colors[0] = "tab:blue"
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Throws", color=colors[0])
line1, = ax1.plot(df_spieler["Year"], df_spieler["Total"], label="Number of Throws", color=colors[0])
ax1.tick_params(axis="y", labelcolor=colors[0])

# **Zweite y-Achse für die Doppelquote**
ax2 = ax1.twinx()
#colors[1] = "tab:red"
ax2.set_ylabel("Double Quota", color=colors[1])
line2, = ax2.plot(df_spieler["Year"], df_spieler["Double Quota"], label="Double Quota", color=colors[1], linestyle="dashed")
ax2.tick_params(axis="y", labelcolor=colors[1])

# **Gemeinsame Legende erstellen**
lines = [line1, line2]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc="upper left")

# Titel setzen
plt.title(f"Number of Throws and Double Quota from {spieler_name} on D {double_value}")

# Diagramm anzeigen
plt.show()
