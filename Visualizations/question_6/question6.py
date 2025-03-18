import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def ranking_age():
    def format_name(name):
        # only change format if name contains comma
        if "," in name:
            surname, first_name = name.split(", ", 1)  # divide name
            surname = surname.capitalize()  # only first letter is capitalized
            first_name = first_name.strip() 
            return f"{first_name} {surname}" #combine name again
        
        return name.strip()

    list_player = []
    for year in range(2009, 2025):
        file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'
        df = pd.read_csv(file)
        name = df[(df['Aktuelle Position'] == 1)]['Name'].iloc[0]
        list_player.append(format_name(name))
    
    file_players = 'Data/question 6/male_players.csv'
    df_players = pd.read_csv(file_players)

    nationalities_general = ['England', 'Portugal', 'Deutschland', 'Schottland', 'Niederlande', 'Irland', 'Schweiz', 'Anderes']
    nationalities = nationalities_general
    order_of_merit = []
    counter = []
    for i in range(2):
        total = 0
        for country in nationalities_general[:len(nationalities_general)-1]:
            counter_value = df_players['Nationality'].value_counts().get(country, 0)
            counter.append(counter_value)
            '''for j in range(counter_value):
                nationalities.append(country)'''
            total += counter_value
            order_of_merit.append(i+1)
        counter.append(len(df_players)- total)
        order_of_merit.append(i+1)
    
    fig = go.Figure()
    colors = px.colors.qualitative.Prism
    
    fig.add_trace(go.Scatter(
    x=nationalities,
    y=order_of_merit,
    mode="markers",  # Nur Punkte (keine Linien)
    marker=dict(
        size=[s / 2 for s in counter],  # Blasengröße (angepasst für bessere Skalierung)
        color=order_of_merit,  # Farbverlauf basierend auf der Quote
        colorscale=colors,  # Farbschema
        showscale=True  # Farblegende anzeigen
    ),
    text=[f"Spiele: {s}" for s in counter],  # Hover-Text
    ))

    # Layout anpassen
    fig.update_layout(
        title="Blasendiagramm: Checkout-Quote über die Jahre",
        xaxis_title="Jahr",
        yaxis_title="Checkout-Quote (%)",
        yaxis_tickformat=".0%",  # Prozentwerte auf Y-Achse
        template="plotly_white"
    )

    return fig

fig = ranking_age()
fig.show()