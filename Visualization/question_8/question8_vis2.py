import pandas as pd
import matplotlib.pyplot as plt
import pycountry

countries = {}

def get_country_code(country_name):
    ioc_mapping = {
        "DEU": "GER",  # Germany
        "CHE": "SUI",   # Switzerland
        "GRC": "GRE",
        "KOR": "KOR",  # South Korea
        "PRK": "PRK",  # North Korea
        "ZAF": "RSA",  # South Africa
        "IRN": "IRI",
        "NLD": "NED"
    }
    
    countries_not_in_iso = {
        "England": "ENG",
        "Scotland": "SCO",
        "Wales": "WAL",
        "Northern Ireland": "NIR",
        "Russia": "RUS",
        "Chinese Taipei": "CHI", 
        "Netherlands": "NED"
    }

    try:
        country = pycountry.countries.get(name=country_name)
        if country_name in countries_not_in_iso:
            country = countries_not_in_iso[country_name]
            return country
        if country in ioc_mapping:
            country = ioc_mapping[country]
        else:
            country = country.alpha_3  # gibt das 3-Buchstaben-Kürzel zurück
        countries[country_name] = country
        return country
    except AttributeError:
        return None  # falls das Land nicht gefunden wird

# CSV-Dateien einlesen
player_data = pd.read_csv('./Data/Darts_Orakel_Stats/Checkout Pcnt.csv')
country_data = pd.read_csv('./Data/Darts_Orakel_Stats/world_cup_Checkout Pcnt.csv')

# Länder in der 'Player' Spalte der zweiten CSV identifizieren
#country_data['Country'] = country_data['Player'].where(country_data['Country'].isna(), country_data['Country'])

# DataFrames für Spieler und Länder erstellen
players_df = country_data[country_data['Country'].notna()]  # Nur Spieler
countries_df = country_data[country_data['Country'].isna()]  # Nur Länder

# Anwendung der Funktion auf die 'Country'-Spalte und Erstellung einer neuen 'Country_Code'-Spalte
countries_df['Country'] = countries_df['Player'].apply(get_country_code)

# Spieler aus der ersten CSV, die auch in der zweiten CSV vorkommen
players_in_both = player_data[player_data['Player'].isin(players_df['Player'])]

# Überprüfen, ob Spieler vorhanden sind
print(f"Anzahl Spieler, die in beiden DataFrames vorkommen: {len(players_in_both)}")

# Merge der beiden DataFrames basierend auf Jahr und Land
merged_df = pd.merge(players_in_both, countries_df, on=['Country', 'Year'], suffixes=('_player', '_country'))

# Überprüfen, ob der Merge funktioniert hat
print(f"Anzahl der Zeilen im zusammengeführten DataFrame: {len(merged_df)}")

# Konvertiere die Prozentwerte in numerische Werte
merged_df['Stat_player'] = merged_df['Stat_player'].str.replace('%', '').astype(float)
merged_df['Stat_country'] = merged_df['Stat_country'].str.replace('%', '').astype(float)

# Vergleichen der Statistiken
merged_df['Better_Than_Country'] = merged_df['Stat_player'] > merged_df['Stat_country']

# Zählen der besseren und schlechteren Spieler für jedes Land
comparison_counts = merged_df.groupby('Country').agg(
    better_count=('Better_Than_Country', 'sum'),
    worse_count=('Better_Than_Country', lambda x: (~x).sum())
).reset_index()

# Überprüfen der Zählergebnisse
#print(comparison_counts)

# Wenn der DataFrame leer ist, stoppen wir den Plot
if comparison_counts.empty:
    print("Es gibt keine Daten zum Plotten.")
else:
    # Balkendiagramm erstellen
    plt.figure(figsize=(10, 6))

    # Positive Balken (bessere Spieler)
    plt.bar(comparison_counts['Country'], comparison_counts['better_count'], color='green', label='Player better than combined Checkout Quota')

    # Negative Balken (schlechtere Spieler)
    plt.bar(comparison_counts['Country'], -comparison_counts['worse_count'], color='red', label='Player worse')

    plt.xlabel('Country')
    plt.ylabel('Number of Players summed up over the years')
    plt.title("Comparison between the Player's Checkout and the Team Checkout Quota in the World Cup (Checkout %)")
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.show()