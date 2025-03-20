import pandas as pd
import glob
import os

# Pfad zum Ordner mit den CSV-Dateien
folder_path = "Data/Flashcore/"  # Ersetze mit dem tatsächlichen Pfad
output_file = "Visualizations/question_10/180_stats.csv"  # Zieldatei für die Ergebnisse

# Alle CSV-Dateien im Ordner finden
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# Liste für Ergebnisse
results = []

# Verarbeitung jeder Datei
for file in csv_files:
    df = pd.read_csv(file)
    
    # Vorherigen "Leg Value" für jedes Leg hinzufügen
    df["Prev Leg Value"] = df.groupby('Leg')['Leg Value'].shift(1)
    
    # Falls der erste Wert als NaN erscheint, optional mit 0 oder einem anderen Wert ersetzen
    df["Prev Leg Value"].fillna("0-0", inplace=True)
    
    # Leg Value in zwei Spalten für Vergleich aufteilen
    df[["Home Score", "Away Score"]] = df["Leg Value"].str.split("-", expand=True).astype(int)
    df[["Prev Home Score", "Prev Away Score"]] = df["Prev Leg Value"].str.split("-", expand=True).astype(int)
    
    # Bestimmung des Siegers eines Legs
    df["Leg Winner"] = df.apply(lambda row: "Home" if row["Home Score"] > row["Prev Home Score"] 
                                else ("Away" if row["Away Score"] > row["Prev Away Score"] else "Draw"), axis=1)
    
    # Spalte "First" erstellen: True für die erste Zeile eines Legs, sonst False
    df["First"] = df["Leg Value"] != df["Prev Leg Value"]
    
    # Spalten für 180er-Würfe filtern
    df["180 Home"] = df["Throw Home"] == 180
    df["180 Away"] = df["Throw Away"] == 180
    df["180"] = df["180 Home"] | df["180 Away"]
    df["180 Player"] = df.apply(lambda row: "Home" if row["180 Home"] else ("Away" if row["180 Away"] else None), axis=1)
    
    # Fälle zählen, in denen der erste 180-Werfer auch das Leg gewonnen hat
    total_legs_180 = ((df["First"] == True) & (df["180"] == True)).sum()
    wins_after_180 = ((df["First"] == True) & (df["180 Player"] == df["Leg Winner"])).sum()
    
    # Wahrscheinlichkeit berechnen und in Prozent umwandeln
    probability = (wins_after_180 / total_legs_180 * 100) if total_legs_180 > 0 else 0
    
    # Durchschnittswert berechnen und in Prozent umwandeln
    avg_probability = (wins_after_180 / total_legs_180 * 100) if total_legs_180 > 0 else 0
    
    # Dateiname als Turniernamen extrahieren (ohne ".csv")
    tournament_name = os.path.splitext(os.path.basename(file))[0]
    
    # Ergebnisse speichern
    results.append([tournament_name, total_legs_180, wins_after_180, probability, avg_probability])

# Ergebnisse als DataFrame speichern
results_df = pd.DataFrame(results, columns=["Tournament", "Total Legs 180", "Wins After 180", "Probability (%)", "Avg Probability"])

# Durchschnittswerte für alle Turniere berechnen und in Prozent umwandeln
avg_total_legs_180 = round(results_df["Total Legs 180"].mean(), 2)
avg_wins_after_180 = round(results_df["Wins After 180"].mean(), 2)
avg_probability = round(results_df["Probability (%)"].mean(), 2)
avg_avg_probability = round(results_df["Avg Probability"].mean(), 2)

# Zeile mit Gesamt-Durchschnittswerten hinzufügen
average_row = pd.DataFrame([["Average", avg_total_legs_180, avg_wins_after_180, avg_probability, avg_avg_probability]],
                           columns=results_df.columns)

# Durchschnittszeile an die Tabelle anhängen
results_df = pd.concat([results_df, average_row], ignore_index=True)

# CSV-Datei speichern
results_df.to_csv(output_file, index=False)

print(f"Ergebnisse gespeichert in {output_file}")
