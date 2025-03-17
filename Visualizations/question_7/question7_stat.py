import pandas as pd
import scipy.stats as stats
import plotly.express as px

def chi_squared():

    # CSV-Datei einlesen
    df = pd.read_csv('Visualization/question 7/question7_table.csv', index_col=0)

    # Überprüfen der Struktur
    print(df.head())

    # Chi-Quadrat-Test der Unabhängigkeit durchführen
    chi2, p, dof, expected = stats.chi2_contingency(df)

    # Ergebnisse ausgeben
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
    
    return df, observed_vs_expected

# Die Differenzen ausgeben (Optional)
#print(observed_vs_expected)

def plot_observed_frequencies():
    df, _ = chi_squared()
    
    # 📊 HEATMAP 1: Beobachtete Häufigkeiten
    fig1 = px.imshow(df,
                    labels=dict(x="Nationalität", y="Austragungsland", color="Häufigkeit"),
                    x=df.columns,
                    y=df.index,
                    title="Beobachtete Häufigkeiten zwischen Austragungsland und Nationalität",
                    color_continuous_scale="YlGnBu",
                    text_auto=True)
    
    return fig1
    
#fig1.show()

def plot_observed_expected_frequencies():
    df, observed_vs_expected = chi_squared()
    
    # 📊 HEATMAP 2: Differenzen zwischen Beobachtet & Erwartet
    fig2 = px.imshow(observed_vs_expected,
                    labels=dict(x="Nationalität", y="Austragungsland", color="Differenz"),
                    x=df.columns,
                    y=df.index,
                    title="Differenzen zwischen Beobachteten und Erwarteten Häufigkeiten",
                    color_continuous_scale="coolwarm",
                    text_auto=".2f")
    
    return fig2
    
#fig2.show()


def plot_conditional_probability():
    df, _ = chi_squared()
    
    # Bedingte Wahrscheinlichkeiten berechnen (P(Nationalität | Austragungsland))
    conditional_probabilities = df.div(df.sum(axis=1), axis=0)

    # 📊 HEATMAP 3: Bedingte Wahrscheinlichkeiten
    fig3 = px.imshow(conditional_probabilities,
                    labels=dict(x="Nationalität", y="Austragungsland", color="Wahrscheinlichkeit"),
                    x=df.columns,
                    y=df.index,
                    title="Bedingte Wahrscheinlichkeiten zwischen Austragungsland und Nationalität",
                    color_continuous_scale="viridis",
                    text_auto=".2f")
    
    return fig3
    
#fig3.show()
