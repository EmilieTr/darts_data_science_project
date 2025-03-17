import pycountry
import csv

# Datei erstellen und Ländercodes schreiben
with open("Data/question 8/question8.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Country", "Alpha-3 Code"])  # Spaltenüberschriften
    
    for country in pycountry.countries:
        writer.writerow([country.name, country.alpha_3])

print("CSV-Datei wurde erfolgreich erstellt: country_codes.csv")
