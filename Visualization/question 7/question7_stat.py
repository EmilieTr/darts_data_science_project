import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

# CSV-Datei einlesen
df = pd.read_csv('Data/question 7/question7_table.csv', index_col=0)

# Überprüfen der Struktur
print(df.head())

# Chi-Quadrat-Test der Unabhängigkeit durchführen
chi2, p, dof, expected = stats.chi2_contingency(df)

# Ergebnisse anzeigen
print(f"Chi-Quadrat-Wert: {chi2}")
print(f"p-Wert: {p}")
print(f"Freiheitsgrade: {dof}")
print("Erwartete Häufigkeiten:")
print(expected)

# p-Wert interpretieren
alpha = 0.05  # Signifikanzniveau
if p < alpha:
    print("Es besteht eine signifikante Beziehung zwischen Austragungsland und Nationalität.")
else:
    print("Es besteht keine signifikante Beziehung zwischen Austragungsland und Nationalität.")


# Differenz zwischen beobachteten und erwarteten Häufigkeiten berechnen
observed_vs_expected = df - expected

# Die Differenzen ausgeben (Optional)
print(observed_vs_expected)


# Heatmap der beobachteten Häufigkeiten
plt.figure(figsize=(10, 8))
sns.heatmap(df, annot=True, fmt='d', cmap="YlGnBu", linewidths=0.5)
plt.title('Beobachtete Häufigkeiten zwischen Austragungsland und Nationalität')
plt.show()

# Heatmap der Differenz zwischen beobachteten und erwarteten Häufigkeiten
plt.figure(figsize=(10, 8))
sns.heatmap(observed_vs_expected, annot=True, fmt='.2f', cmap="coolwarm", linewidths=0.5)
plt.title('Differenzen zwischen Beobachteten und Erwarteten Häufigkeiten')
plt.show()


# Bedingte Wahrscheinlichkeiten berechnen (P(Nationalität | Austragungsland))
conditional_probabilities = df.div(df.sum(axis=1), axis=0)

# Heatmap der bedingten Wahrscheinlichkeiten
plt.figure(figsize=(10, 8))
sns.heatmap(conditional_probabilities, annot=True, fmt='.2f', cmap="viridis", linewidths=0.5)
plt.title('Bedingte Wahrscheinlichkeiten zwischen Austragungsland und Nationalität')
plt.show()
