import pandas as pd
from question7_countries_of_venues import countries_of_venues

df = pd.read_csv(
    "Visualizations/question_7/question7_countries_to_venues.csv"
)

# Cross-tabulation of host countries and winner nationalities
cross_tab = pd.crosstab(
    df['Austragungsland'],
    df['Nationalität'],
    margins=True,
    margins_name="Total"
)

# Tabelle im Terminal ausgeben
print(cross_tab.to_string())

# Save cross table to CSV
cross_tab.to_csv(
    "Visualizations/question_7/question7_table.csv",
    index=True
)