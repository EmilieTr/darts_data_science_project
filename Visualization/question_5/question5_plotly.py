import pandas as pd
import plotly.graph_objects as go

# CSV-Datei laden
file = 'Data/question5.csv'
df = pd.read_csv(file)
print(df.head())

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

# Diagramm anzeigen
fig.show()
