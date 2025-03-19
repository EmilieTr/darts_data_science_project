import pandas as pd
from question7_countries_of_venues import countries_of_venues

df = pd.read_csv("Visualizations/question_7/question7_countries_to_venues.csv")

# Kreuztabelle der Austragungsländer und Sieger-Nationalitäten
cross_tab = pd.crosstab(df['Austragungsland'], df['Nationalität'], margins=True, margins_name="Total")

# Tabelle im Terminal ausgeben
print(cross_tab.to_string())  # .to_string() sorgt dafür, dass die Tabelle im Terminal schön formatiert wird

# Speichern der Kreuztabelle als CSV-Datei
cross_tab.to_csv("Visualizations/question_7/question7_table.csv", index=True)  # `index=True` behält den Index bei