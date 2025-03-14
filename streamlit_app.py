import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# CSV-Datei laden
file = 'data/question5.csv'
df = pd.read_csv(file)
st.write(df.head())  # Gibt die ersten Zeilen der CSV in Streamlit aus

# Daten nach Jahr gruppieren
participants_per_year = df.groupby('Year')['Participants'].mean()

# Erstellen der Plotly-Grafik
fig = go.Figure()

# Linie erstellen
fig.add_trace(go.Scatter(x=participants_per_year.index,
                         y=participants_per_year.values,
                         mode='lines',
                         name='Participants',
                         line=dict(color='blue')))

# Achsenbeschriftungen und Titel
fig.update_layout(
    title="Development of participants over the years",
    xaxis_title="Year",
    yaxis_title="Participants",
    legend=dict(title='Participants', x=1, y=1, traceorder='normal', font=dict(size=8), bordercolor="Black", borderwidth=1),
    showlegend=True
)

# Diagramm in Streamlit anzeigen
st.plotly_chart(fig)
