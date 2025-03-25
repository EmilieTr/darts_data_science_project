import pandas as pd

df = pd.read_csv(
    "Visualizations/question_7/question7_countries_to_venues.csv"
    )

# Count frequency of host countries
land_counts = df["Austragungsland"].value_counts().reset_index()

# Rename columns
land_counts.columns = ["Austragungsland", "Anzahl"]

# Save to CSV file
land_counts.to_csv(
    "Visualizations/question_7/question7_countries_number.csv",
    index=False
)