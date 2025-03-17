import pandas as pd
import plotly.graph_objects as go

def plot_price_money():

    # Funktion zur Umwandlung von Währungsstrings in Float-Werte
    def convert_currency(value):
        if isinstance(value, str):
            value = value.replace('£', '').replace(',', '')
            return float(value)
        return value

    # CSV-Datei laden
    file = 'Data/question 5/question5.csv'
    df = pd.read_csv(file)

    # Preisgeld-Spalten und zugehörige Labels definieren
    columns = ['Champion', 'Runner-up', '3d place', '4d place', 'Quarter finalists', 
            'Last 16', 'Last 24', 'Last 32', 'Last 64', 'Last 96']
    labels = ['1st', '2nd', '3rd', '4th', 'Quarter finalists', 'Last 16', 
            'Last 24', 'Last 32', 'Last 64', 'Last 96']

    # Daten konvertieren
    for column in columns:
        df[column] = df[column].apply(convert_currency)
    df['Semi finalists'] = df['Semi finalists'].apply(convert_currency)
    df['Total Prize Pool'] = df['Total Prize Pool'].apply(convert_currency)

    # Fehlende Werte behandeln
    columns_without_3rd_4th = [col for col in columns if col not in ['3d place', '4d place']]
    df[columns_without_3rd_4th] = df[columns_without_3rd_4th].fillna(0)
    df['3d place'].fillna(df['Semi finalists'], inplace=True)
    df['4d place'].fillna(df['Semi finalists'], inplace=True)

    # **Stacked Bar Chart mit Plotly**
    fig = go.Figure()

    # Werte für gestapeltes Diagramm berechnen
    bottom_values = [0] * len(df['Year'])  # Basiswert für jede Kategorie

    # **Balken für jede Preisgeld-Kategorie hinzufügen**
    for column, label in zip(columns, labels):
        fig.add_trace(go.Bar(
            x=df['Year'],
            y=df[column],
            name=label,
            text=df[column],
            textposition='auto'
        ))

    # Fehlendes Preisgeld auffüllen
    missing_prize_money = df['Total Prize Pool'] - df[columns].sum(axis=1)
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=missing_prize_money,
        name="Other Prize Money",
        marker_color='gray',
        opacity=0.6
    ))

    # **Layout anpassen**
    fig.update_layout(
        title="Development of Prize Money over the Years (PDC World Championship)",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Prize Money (£)", tickformat=","),
        barmode='stack',  # Stacked Bar Chart
        legend=dict(x=1, y=1),
        template="plotly_white"
    )

    return fig

# **Diagramm anzeigen (für Streamlit: st.plotly_chart(fig))**
#fig.show()
