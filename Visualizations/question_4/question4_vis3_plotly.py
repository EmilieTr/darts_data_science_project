import pandas as pd
import plotly.express as px

# CSV-Daten einlesen
csv_data = "./Data/question 4/question4_doubles.csv"
df = pd.read_csv(csv_data)

# Nur relevante Daten (Treffer >= 100) behalten
df_filtered = df[df["Hit"] >= 100]

# Linien-Diagramm mit Plotly erstellen
fig = px.line(
    df_filtered, 
    x="Year", 
    y="Hit", 
    color="Double", 
    markers=True,  # Punkte anzeigen
    title="Entwicklung der Hit-Werte über die Jahre",
    labels={"Year": "Jahr", "Hit": "Hit-Wert", "Double": "Doppelfeld"},
    line_shape="linear"
)

# Diagramm anzeigen
fig.show()
