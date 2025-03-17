import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV-Datei einlesen
data = pd.read_csv("./Data/Darts_Orakel_Stats/world_cup_Checkout Pcnt.csv")

# Entfernen von leeren Werten
data.dropna(subset=['Country', 'Stat', 'Year'], inplace=True)

# Umwandeln der Stat-Werte in numerische Werte
data['Stat'] = data['Stat'].str.replace('%', '').astype(float)

# Erstellen einer neuen DataFrame für Länder-Statistiken, gruppiert nach Jahr
country_stats = data.groupby(['Country', 'Year'])['Stat'].mean().reset_index()

# Kombinieren der Spieler und Länder-Daten
player_stats = data[['Player', 'Country', 'Stat', 'Year']]
combined_data = pd.merge(player_stats, country_stats[['Country', 'Year', 'Stat']], on=['Country', 'Year'], suffixes=('_Player', '_Country'))

# Berechnen, ob der Spieler besser oder schlechter als das Land ist
combined_data['BetterThanCountry'] = combined_data['Stat_Player'] > combined_data['Stat_Country']

# Berechnen des Unterschieds und Anwenden des 5%-Filters
combined_data['StatDifference'] = abs(combined_data['Stat_Player'] - combined_data['Stat_Country'])
combined_data['SignificantDifference'] = combined_data['StatDifference'] >= 5

# Nur Spieler mit einer signifikanten Abweichung von 5% berücksichtigen
filtered_data = combined_data[combined_data['SignificantDifference']]

# Berechnen der Anzahl der Spieler, die besser und schlechter als das Land sind
better_players = filtered_data.groupby(['Country', 'Year'])['BetterThanCountry'].sum().reset_index()
worse_players = filtered_data.groupby(['Country', 'Year'])['BetterThanCountry'].apply(lambda x: len(x) - x.sum()).reset_index()

# Zusammenführen der beiden DataFrames
country_player_count = pd.merge(better_players, worse_players, on=['Country', 'Year'], suffixes=('_Better', '_Worse'))

# Erstellen einer neuen Spalte für negative Werte der "schlechteren" Spieler
country_player_count['WorseThanCountry_Neg'] = -country_player_count['BetterThanCountry_Worse']

# Visualisierung
plt.figure(figsize=(12, 8))

# Balken für bessere Spieler (einheitliche blaue Farbe)
sns.barplot(data=country_player_count, x='Country', y='BetterThanCountry_Better', color='blue', ci=None)

# Balken für schlechtere Spieler (einheitliche rote Farbe)
sns.barplot(data=country_player_count, x='Country', y='WorseThanCountry_Neg', color='red', ci=None)

# Visualisierung anpassen
plt.axhline(0, color='gray', linewidth=1)
plt.xlabel('Country')
plt.ylabel('Number of Players')
plt.title('Players Better and Worse than Country Stats (with 5% Difference) for the Same Year')

# Achsentitel und Layout anpassen
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
