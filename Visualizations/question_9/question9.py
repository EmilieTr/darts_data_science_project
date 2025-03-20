import pandas as pd
import glob
import os

# Pfad zum Ordner mit den CSV-Dateien
folder_path = "Data/Flashcore/"
output_file = "Visualizations/question_9/180_stats.csv"

# Alle CSV-Dateien im Ordner finden
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# Liste für Ergebnisse
results = []

# Verarbeitung jeder Datei
for file in csv_files:
    df = pd.read_csv(file)
    
    # Spalten für 180er-Würfe filtern
    df["180_Home"] = df["Throw Home"] == 180
    df["180_Away"] = df["Throw Away"] == 180
    df["180"] = df["180_Home"] | df["180_Away"]
    
    # Anzahl der 180er-Würfe zählen
    total_180s = df["180"].sum()
    
    # Zählen, wie oft zwei 180er hintereinander geworfen wurden
    consecutive_180s = (df["180"] & df["180"].shift(-1)).sum()
    
    # Wahrscheinlichkeit berechnen und als Prozentwert speichern
    probability = round((consecutive_180s / total_180s) * 100, 2) if total_180s > 0 else 0

    # Durchschnittswert berechnen
    avg_consecutive = round(consecutive_180s / total_180s, 2) if total_180s > 0 else 0

    # Dateiname als Turniernamen extrahieren (ohne ".csv")
    tournament_name = os.path.splitext(os.path.basename(file))[0]
    
    # Ergebnisse speichern
    results.append([tournament_name, total_180s, consecutive_180s, probability, avg_consecutive])

# Ergebnisse als DataFrame speichern
results_df = pd.DataFrame(results, columns=["Tournament", "Total 180s", "Consecutive 180s", "Probability (%)", "Avg Consecutive"])

# Durchschnittswerte für alle Turniere berechnen
avg_total_180s = round(results_df["Total 180s"].mean(), 2)
avg_consecutive_180s = round(results_df["Consecutive 180s"].mean(), 2)
avg_probability = round(results_df["Probability (%)"].mean(), 2)
avg_avg_consecutive = round(results_df["Avg Consecutive"].mean(), 2)

# Zeile mit Gesamt-Durchschnittswerten hinzufügen
average_row = pd.DataFrame([["Average", avg_total_180s, avg_consecutive_180s, avg_probability, avg_avg_consecutive]],
                           columns=results_df.columns)

# Durchschnittszeile an die Tabelle anhängen
results_df = pd.concat([results_df, average_row], ignore_index=True)

# CSV-Datei speichern
results_df.to_csv(output_file, index=False)

print(f"Ergebnisse gespeichert in {output_file}")
