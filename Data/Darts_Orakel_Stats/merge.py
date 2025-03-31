import pandas as pd

# Dateien laden
file1 = "Data/darts_orakel_stats/player_averages.csv"
file2 = "Data/darts_orakel_stats/player_averages_new.csv"

# CSV-Dateien einlesen
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Vereinigung der beiden DataFrames ohne Duplikate basierend auf den Spalten 'Player' und 'Year'
merged_df = pd.concat([df1, df2]).drop_duplicates(subset=['Player', 'Year'])

# Aufsteigend nach 'Player' und 'Year' sortieren
merged_df = merged_df.sort_values(by=['Year', 'Rank'], ascending=[True, True])

# Das Ergebnis in einer neuen CSV-Datei speichern
merged_df.to_csv("Data/darts_orakel_stats/merged_file.csv", index=False)

print("Die Vereinigung der Dateien wurde erfolgreich in 'merged_file.csv' gespeichert und aufsteigend sortiert.")
