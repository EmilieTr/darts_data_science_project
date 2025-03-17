import pandas as pd
import plotly.graph_objects as go

def plot_price_money_and_participants():

    # Funktion zur Umwandlung von Währungsstrings in float
    def convert_currency(value):
        if isinstance(value, str):
            value = value.replace('£', '').replace(',', '')
            return float(value)
        return value

    # CSV-Datei laden
    file = 'Data/question 5/question5.csv'
    df = pd.read_csv(file)

    # Preisgeld-Spalten definieren
    columns = ['Champion', 'Runner-up', '3d place', '4d place', 'Quarter finalists', 
            'Last 16', 'Last 24', 'Last 32', 'Last 64', 'Last 96']
    labels = ['1st', '2nd', '3rd', '4th', 'Quarter finalists', 'Last 16', 
            'Last 24', 'Last 32', 'Last 64', 'Last 96']

    # Daten umwandeln
    for column in columns:
        df[column] = df[column].apply(convert_currency)
    df['Semi finalists'] = df['Semi finalists'].apply(convert_currency)
    df['Total Prize Pool'] = df['Total Prize Pool'].apply(convert_currency)

    # Fehlende Werte auffüllen
    columns_without_3rd_4th = [col for col in columns if col not in ['3d place', '4d place']]
    df[columns_without_3rd_4th] = df[columns_without_3rd_4th].fillna(0)
    df['3d place'].fillna(df['Semi finalists'], inplace=True)
    df['4d place'].fillna(df['Semi finalists'], inplace=True)

    # Teilnehmer-Daten gruppieren
    participants_per_year = df.groupby('Year')['Participants'].mean()

    # **Plotly-Figur erstellen**
    fig = go.Figure()

    # **Gestapeltes Balkendiagramm für Preisgelder**
    bottom_values = [0] * len(df['Year'])  # Startwerte für Stapel

    for column, label in zip(columns, labels):
        fig.add_trace(go.Bar(
            x=df['Year'],
            y=df[column],
            name=label,
            marker=dict(line=dict(width=0.5))
        ))
        bottom_values = [sum(x) for x in zip(bottom_values, df[column])]

    # Fehlendes Preisgeld auffüllen
    missing_prize_money = df['Total Prize Pool'] - bottom_values
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=missing_prize_money,
        name="Other Prize Money",
        marker=dict(color='gray', opacity=0.6)
    ))

    # **Linienplot für Teilnehmerzahlen (zweite Y-Achse)**
    fig.add_trace(go.Scatter(
        x=participants_per_year.index,
        y=participants_per_year.values,
        mode='lines+markers',
        name='Participants',
        yaxis='y2',
        line=dict(color='red', width=2)
    ))

    # **Layout anpassen**
    fig.update_layout(
        title="Development of Prize Money and Participants over the Years (PDC World Championship)",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Prize Money (£)", side="left"),
        yaxis2=dict(
            title="Participants",
            overlaying="y",
            side="right"
        ),
        barmode="stack",  # Stacked Bar Chart
        legend=dict(x=1.1, y=1),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

# **Diagramm anzeigen (in Streamlit verwenden mit st.plotly_chart(fig))**
#fig.show()