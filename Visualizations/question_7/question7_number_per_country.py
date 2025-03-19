import pandas as pd

df = pd.read_csv("Visualizations/question_7/question7_countries_to_venues.csv")

# Zählen der Häufigkeit jedes Austragungslandes
land_counts = df["Austragungsland"].value_counts().reset_index()

# Spalten umbenennen
land_counts.columns = ["Austragungsland", "Anzahl"]

# Speichern in eine neue CSV-Datei
land_counts.to_csv("Visualizations/question_7/question7_countries_number.csv", index=False)