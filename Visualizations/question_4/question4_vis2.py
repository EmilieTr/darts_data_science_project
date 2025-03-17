import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#csv_data = "./Data/question4.csv"
csv_data = "./Data/question 4/question4_doubles.csv"

# CSV-Daten einlesen
df = pd.read_csv(csv_data)  # Ersetze mit dem tatsächlichen Dateipfad


# Vis 1
# Neue Spalte mit der Gesamtanzahl der Würfe pro Spieler
df["Total"] = df["Hit"] + df["Single"] + df["Outside"] + df["Other"]

# Bestes Doppelfeld für jeden Spieler ermitteln
df_max = df.loc[df.groupby("Player")["Total"].idxmax(), ["Player", "Double", "Hit"]]

# Häufigkeit der Doppelfelder zählen
double_counts = df_max["Double"].value_counts()

# Werte unter 3% als "Sonstige" zusammenfassen
total_count = double_counts.sum()
double_counts_filtered = double_counts[double_counts / total_count >= 0.015]
other_count = double_counts[double_counts / total_count < 0.015].sum()

if other_count > 0:
    double_counts_filtered["Others"] = other_count


# Vis 2
# Neue Spalte mit der Gesamtanzahl der Würfe pro Spieler
df["Total"] = df["Hit"] + df["Single"] + df["Outside"] + df["Other"]

# Bestes Doppelfeld für jeden Spieler ermitteln
df_max2 = df.loc[df.groupby("Player")["Total"].idxmax(), ["Player", "Double", "Hit"]]

# Häufigkeit der Doppelfelder zählen
double_counts2 = df_max2["Double"].value_counts()

# Werte unter 3% als "Sonstige" zusammenfassen
total_count2 = double_counts2.sum()
double_counts_filtered2 = double_counts2[double_counts2 / total_count2 >= 0.015]
other_count2 = double_counts[double_counts2 / total_count2 < 0.015].sum()

if other_count > 0:
    double_counts_filtered["Others"] = other_count



# Farben aus der "Paired"-Colormap
if len(double_counts_filtered) > len(double_counts_filtered2):
    colors = plt.get_cmap("Paired")(np.linspace(0, 1, len(double_counts_filtered)))
else:
    colors = plt.get_cmap("Paired")(np.linspace(0, 1, len(double_counts_filtered2)))

# Index anpassen
double_counts_filtered.index = double_counts_filtered.index.map(lambda x: f"D {x}")
double_counts_filtered2.index = double_counts_filtered2.index.map(lambda x: f"D {x}")

# Erstellen der Pie-Charts
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Pie-Chart 1: Häufigkeit der genutzten Doppelfelder
axes[0].pie(double_counts_filtered, labels=double_counts_filtered.index, autopct="%1.1f%%", colors=colors)
axes[0].set_title("Distribution of the Throws on the Double Fields")

# Pie-Chart 2: Treffer (Hit) für diese Doppelfelder
axes[1].pie(double_counts_filtered2, labels=double_counts_filtered2.index, autopct="%1.1f%%", colors=colors)
axes[1].set_title("Distribution of the Hits on the Double Fields")

# Diagramme anzeigen
plt.show()

