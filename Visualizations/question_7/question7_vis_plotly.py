import pandas as pd
from geopy.geocoders import Nominatim
import time  # Für Verzögerung zwischen Anfragen

# CSV einlesen
df1 = pd.read_csv("./Data/question 7/question7_majors.csv")
df2 = pd.read_csv("./Data/question 7/question7_european_tour.csv")

df = pd.concat([df1, df2], ignore_index=True)

# Geocoder initialisieren
geolocator = Nominatim(user_agent="geo_finder")

# Funktion zur Bestimmung des Landes aus der Stadt
def get_country(city):
    try:
        location = geolocator.geocode(city, language='en')
        if location:
            return location.address.split(",")[-1].strip()  # Land aus der Adresse extrahieren
    except:
        return None  # Falls keine Daten gefunden werden
    return None

# Stadt aus der Spalte "Austragungsort" extrahieren (mit Prüfung auf NaN oder ungültige Werte)
df['Stadt'] = df['Austragungsort'].apply(lambda x: x.split(",")[-1].strip() if isinstance(x, str) else None)

# Länder für jede Stadt bestimmen (mit Verzögerung, um API-Limits zu vermeiden)
df['Austragungsland'] = df['Stadt'].apply(lambda city: get_country(city) if pd.notna(city) else None)

# Verzögerung zwischen den Anfragen, um API-Limits zu respektieren
time.sleep(1)

# Kreuztabelle der Austragungsländer und Sieger-Nationalitäten
cross_tab = pd.crosstab(df['Austragungsland'], df['Nationalität'], margins=True, margins_name="Total")

# Tabelle im Terminal ausgeben
print(cross_tab.to_string())  # .to_string() sorgt dafür, dass die Tabelle im Terminal schön formatiert wird

# Speichern der Kreuztabelle als CSV-Datei
cross_tab.to_csv("Visualization/question7/question7_table.csv", index=True)  # `index=True` behält den Index bei