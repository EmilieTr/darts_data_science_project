import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
from datetime import datetime
def plot_ranking_age(var):
    def format_name(name):

        # change different formats of names into one format (all lowercase and "first_name surname")
        # lowercase for avoiding errors with more than one surname
        if "," in name:
            if ", " in name: # sometimes there is no space between the comma and the next name
                surname, first_name = name.split(", ", 1)  # divide name
            else:
                surname, first_name = name.split(",",1) # divide name
            surname = surname.lower()  # every letter is lowercase
            first_name = first_name.strip().lower()  # every letter is lowercase
            return f"{first_name} {surname}" # combine name again
        
        return name.strip().lower() # every letter is lowercase

    # convert every name in the data frame to lowercase letters only
    # same explanation as in def format_name
    def convert_names_to_lowercase(df):
        df['Name'] = df['Name'].str.lower()
        return df
    
    # calculate the age, when only given the birthday
    def calculate_age(birthday):
        # date of today
        today = date.today()
        # birthday in right format
        birthday= datetime.strptime(birthday, "%d.%m.%Y")
        if today.month == birthday.month:
            if today.day >= birthday.day:
                age = today.year - birthday.year
            else:
                age = today.year - birthday.year -1
        elif today.month > birthday.month:
            age = today.year - birthday.year
        else:
            age = today.year - birthday.year -1
        return age
    
    # sorting age in clusters
    def sorting_in_clusters(birthday):
        age = calculate_age(birthday)
        if age <21: return '10-20'
        elif age <31: return '20-30'
        elif age < 41: return '30-40'
        elif age < 51: return '40-50'
        elif age < 61: return '50-60'
        elif age < 71: return '60-70'
        else: return '70+'

        
    # selection of Age-Clusters with own value on X axis  
    age_selection = ['10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70+']
    
    # lists needed for creating bubble chart
    ages = []
    order_of_merit = []
    counter = []

    # lists for right visualization of Y- axis
    y_axis_tickvals = []
    y_axis_ticktext = []


    # var = number of order_of_merit ranks you want to compare
    for i in range(var):
        # for every rank theres one point on the y-axis
        y_axis_tickvals.append(i+1)
        y_axis_ticktext.append(str(i+1))

        # list of all players who won the specific rank (=var) in order_of_merit in the years 2009 - 2025
        list_player = []
        for year in range(2009, 2025):
            file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'
            df = pd.read_csv(file)
            name = df[(df['Aktuelle Position'] == i+1)]['Name'].iloc[0]
            list_player.append(format_name(name))

        # extracting age of players on list_player
        file_players = 'Data/question 6/male_players.csv'
        df = pd.read_csv(file_players)
        df = convert_names_to_lowercase(df)
        df_players = pd.DataFrame(columns=['Name', 'Age'])
        for player in list_player:
            filtered = df.loc[df['Name'] == player, 'Geburtstag']
            if not filtered.empty:
                age = filtered.iloc[0]
                df_players.loc[len(df_players)] = [player, age]
            else:
                print(f"Spieler {player} nicht gefunden!")
        
        # converting birthday into matching age-cluster
        df_players['Age'] = df_players['Age'].apply(sorting_in_clusters)

        
        for country in age_selection[:len(age_selection)]:
            counter_value = df_players['Age'].value_counts().get(country, 0) # number of players with specific age-cluster
            counter.append(counter_value)
            ages.append(country)
            order_of_merit.append(i+1)

        

    # creating figure
    fig = go.Figure()
    colors = px.colors.qualitative.Prism
    
    fig.add_trace(go.Scatter(
    x=ages,
    y=order_of_merit,
    mode="markers", 
    marker=dict(
        size=[s *5 for s in counter],  # size of bubble (times two for having bigger bubbles)
        color=counter,  # color gradient based on number saved in list counter
        colorscale=colors,
        showscale=True 
    ),
    
    text=[f"Anzahl: {s}" for s in counter],  # hover text
    ))

    # setting the layout
    fig.update_layout(
        title="Correlation of age to rankings",
        xaxis_title="Age",
        yaxis_title="Order of Merit",
        yaxis_tickformat=".",
        #yaxis=dict(showticklabels=False),
        yaxis=dict(tickvals=y_axis_tickvals, ticktext=y_axis_ticktext, showticklabels=True, autorange="reversed"),
        template="plotly_white"
    )

    return fig



var = 20
fig = plot_ranking_age(var)
fig.show()