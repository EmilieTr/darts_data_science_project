import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def ranking_age(var):
    def format_name(name):
        # only change format if name contains comma
        if "," in name:
            surname, first_name = name.split(", ", 1)  # divide name
            surname = surname.lower()  # only first letter is capitalized
            first_name = first_name.strip().lower() 
            return f"{first_name} {surname}" #combine name again
        
        return name.strip().lower()

    def convert_names_to_lowercase(df):
        # Convert all values in the 'Name' column to lowercase
        df['Name'] = df['Name'].str.lower()
        return df

    nationalities_selection = ['England', 'Portugal', 'Deutschland', 'Schottland', 'Niederlande', 'Irland', 'Schweiz', 'Wales', 'Anderes']
    nationalities = []
    order_of_merit = []
    counter = []
    y_axis_tickvals = []
    y_axis_ticktext = []

    for i in range(var):
        y_axis_tickvals.append(i+1)
        y_axis_ticktext.append(str(i+1))
        list_player = []
        for year in range(2009, 2025):
            file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'
            df = pd.read_csv(file)
            name = df[(df['Aktuelle Position'] == i+1)]['Name'].iloc[0]
            list_player.append(format_name(name))
        print(list_player)
        file_players = 'Data/question 6/male_players.csv'
        df = pd.read_csv(file_players)
        df = convert_names_to_lowercase(df)
        df_players = pd.DataFrame(columns=['Name', 'Nationality'])
        for player in list_player:
            filtered = df.loc[df['Name'] == player, 'Nationality']
            
            if not filtered.empty:
                nationality = filtered.iloc[0]
                df_players.loc[len(df_players)] = [player, nationality]
            else:
                print(f"Spieler {player} nicht gefunden!")


        
        
        total = 0
        for country in nationalities_selection[:len(nationalities_selection)-1]:
            counter_value = df_players['Nationality'].value_counts().get(country, 0)
            counter.append(counter_value)
            nationalities.append(country)
            total += counter_value
            order_of_merit.append(i+1)
        counter.append(len(df_players)- total)
        nationalities.append('Anderes')
        order_of_merit.append(i+1)
    #print("nationalities", nationalities)
    #print("order of merit", order_of_merit)
    #print("count", counter)
    
    fig = go.Figure()
    colors = px.colors.qualitative.Prism
    
    fig.add_trace(go.Scatter(
    x=nationalities,
    y=order_of_merit,
    mode="markers",  # Nur Punkte (keine Linien)
    marker=dict(
        size=[s *10 for s in counter],  # Blasengröße (angepasst für bessere Skalierung)
        color=counter,  # Farbverlauf basierend auf der Quote
        colorscale=colors,  # Farbschema
        showscale=True  # Farblegende anzeigen
    ),
    text=[f"Spiele: {s}" for s in counter],  # Hover-Text
    ))

    # Layout anpassen
    fig.update_layout(
        title="Blasendiagramm: How good is which Nationality",
        xaxis_title="Jahr",
        yaxis_title="",
        yaxis_tickformat=".",
        #yaxis=dict(showticklabels=False),
        yaxis=dict(tickvals=y_axis_tickvals, ticktext=y_axis_ticktext, showticklabels=True),
        template="plotly_white"
    )

    return fig

var = 4
fig = ranking_age(var)
fig.show()