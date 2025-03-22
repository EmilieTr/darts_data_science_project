import pandas as pd
import plotly.graph_objects as go
import plotly.express as px  # Import für das Prism-Farbschema

def plot_prize_money_and_participants(selected):

    # Function to convert currency strings to float
    def convert_currency(value):
        if isinstance(value, str):
            value = value.replace('£', '').replace(',', '')
            return float(value)
        return value

    # Load CSV file
    file = 'Data/question 5/question5.csv'
    df = pd.read_csv(file)

    # Define prize money columns
    columns = ['Champion', 'Runner-up', '3d place', '4d place', 'Quarter finalists', 
               'Last 16', 'Last 24', 'Last 32', 'Last 64', 'Last 96']
    labels = ['1st', '2nd', '3rd', '4th', 'Quarter finalists', 'Last 16', 
              'Last 24', 'Last 32', 'Last 64', 'Last 96']

    # Convert currency values
    for column in columns:
        df[column] = df[column].apply(convert_currency)
    df['Semi finalists'] = df['Semi finalists'].apply(convert_currency)
    df['Total Prize Pool'] = df['Total Prize Pool'].apply(convert_currency)

    # Fill missing values
    columns_without_3rd_4th = [col for col in columns if col not in ['3d place', '4d place']]
    df[columns_without_3rd_4th] = df[columns_without_3rd_4th].fillna(0)
    df['3d place'].fillna(df['Semi finalists'], inplace=True)
    df['4d place'].fillna(df['Semi finalists'], inplace=True)

    # Group participant data
    participants_per_year = df.groupby('Year')['Participants'].mean()

    # **Create Plotly figure**
    fig = go.Figure()

    # **Farben aus der Prism-Farbpalette**
    prism_colors = px.colors.qualitative.Prism
    color_count = len(columns)  # Anzahl der Farben, die benötigt werden
    prism_colors = prism_colors[:color_count]  # Anzahl der Farben anpassen

    if "Prize Money" in selected:
        # **Stacked bar chart for prize money**
        bottom_values = [0] * len(df['Year'])  # Starting values for stacking

        for i, (column, label) in enumerate(zip(columns, labels)):
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df[column],
                name=label,  # Legendenname
                marker=dict(color=prism_colors[i % len(prism_colors)], line=dict(width=0)),  # Prism-Farben zuweisen
                hovertemplate='Name: %{data.name}<br>Year: %{x}<br>Prize Money: £%{y:.0f}<br><extra></extra>'  # Hover zeigt name, year, und prize money
            ))
            bottom_values = [sum(x) for x in zip(bottom_values, df[column])]

        # Fill missing prize money
        missing_prize_money = df['Total Prize Pool'] - bottom_values
        fig.add_trace(go.Bar(
            x=df['Year'],
            y=missing_prize_money,
            name="Other Prize Money",
            marker=dict(color='gray', opacity=0.6),
            hovertemplate='Name: %{data.name}<br>Year: %{x}<br>Prize Money: £%{y:.0f}<br><extra></extra>'
        ))

    if "Participants" in selected:
        # **Line plot for participants (second Y-axis)**
        fig.add_trace(go.Scatter(
            x=participants_per_year.index,
            y=participants_per_year.values,
            mode='lines',
            name='Participants',  # Legendenname
            yaxis='y2',
            line=dict(color='red', width=2),
            hovertemplate='Name: %{data.name}<br>Year: %{x}<br>Participants: %{y}<br><extra></extra>'  # Hover zeigt name, year, und participants count
        ))

    # **Adjust layout**
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
        legend=dict(
            x=1.2,  # Legende weiter nach rechts verschoben
            y=1
        ),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig
