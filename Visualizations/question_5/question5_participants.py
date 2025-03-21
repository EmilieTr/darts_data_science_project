import pandas as pd
import plotly.graph_objects as go
import sys
import os

# Gehe eine Ebene nach oben und füge den Pfad zu sys.path hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Jetzt kannst du die Datei importieren
import statistical_analysis


def plot_participants():
    # Load CSV file
    file = 'Data/question 5/question5.csv'
    df = pd.read_csv(file)

    # Group participant data by year
    participants_per_year = df.groupby('Year')['Participants'].mean()

    # **Create Plotly figure**
    fig = go.Figure()



    # **Line plot for participant numbers**
    fig.add_trace(go.Scatter(
        x=participants_per_year.index,
        y=participants_per_year.values,
        mode='lines+markers',
        name='Participants',
        line=dict(color='blue', width=2)
    ))

    # **Adjust layout**
    fig.update_layout(
        title="Development of Participants Over the Years",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Participants"),
        legend=dict(x=1, y=1),
        margin=dict(l=50, r=50, t=50, b=50),
        template="plotly_white"  # Light theme for better visibility
    )
    
    statistical_analysis.all_statistical_tests(participants_per_year.index, participants_per_year.values)

    return fig

plot_participants()