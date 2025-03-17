import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSV-Daten einlesen
csv_data = "./Data/question 4/question4_doubles.csv"
#sv_data = "./Data/question4.csv"  # Ersetze mit dem tatsächlichen Dateipfad

# DataFrame erstellen
df = pd.read_csv(csv_data, header=0)

# Berechnung der Komponenten
df["Miss"] = df["Single"] + df["Outside"] + df["Other"]

# Daten aggregieren nach Doppelfeld
df_agg = df.groupby("Double")[["Miss", "Hit"]].sum().reset_index()

# Farben aus der "Paired"-Colormap
colors = plt.get_cmap("Paired")(np.linspace(0, 1, 2))

# Stacked Bar Chart erstellen
plt.figure(figsize=(8, 5))
plt.bar(df_agg["Double"], df_agg["Hit"], color=colors[0], label="Hit")
plt.bar(df_agg["Double"], df_agg["Miss"], color=colors[1], bottom=df_agg["Hit"], label="Miss")

# Achsenbeschriftung und Titel
plt.xlabel("Double Fields")
plt.ylabel("Number of Throws")
plt.title("Stacked Bar Chart of Hits and Misses per Double Field")
plt.xticks(df_agg["Double"])
plt.legend()

# Diagramm anzeigen
plt.show()
