import pandas as pd
import plotly.graph_objects as go

def plot_participants():

    # CSV-Datei laden
    file = 'Data/question 5/question5.csv'
    df = pd.read_csv(file)

    # Teilnehmer-Daten nach Jahr gruppieren
    participants_per_year = df.groupby('Year')['Participants'].mean()

    # **Plotly-Figur erstellen**
    fig = go.Figure()

    # **Linienplot für Teilnehmerzahlen**
    fig.add_trace(go.Scatter(
        x=participants_per_year.index,
        y=participants_per_year.values,
        mode='lines+markers',
        name='Participants',
        line=dict(color='blue', width=2)
    ))

    # **Layout anpassen**
    fig.update_layout(
        title="Development of Participants Over the Years",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Participants"),
        legend=dict(x=1, y=1),
        margin=dict(l=50, r=50, t=50, b=50),
        template="plotly_white"  # Helles Theme für bessere Sichtbarkeit
    )
    
    return fig

# **Diagramm anzeigen (für Streamlit: st.plotly_chart(fig))**
#fig.show()
