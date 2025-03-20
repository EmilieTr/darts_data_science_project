import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
from datetime import datetime


def plot_ranking_age(var, variant):
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
        if pd.isna(birthday) or birthday is None:
            return None
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
        if age == None: return None
        elif age <21: return '10-20'
        elif age <31: return '20-30'
        elif age < 41: return '30-40'
        elif age < 51: return '40-50'
        elif age < 61: return '50-60'
        elif age < 71: return '60-70'
        else: return '70+'

    
    #function for using proportions and not absolute numbers
    def ratio(ages, total_age, counter):
        for i,age in enumerate(ages):
            if total_age[age] == 0:
                counter[i] = 0
            else:
                counter[i] = counter[i] / total_age[age]
        return counter
    
    def mean_rank(nationalities, order_of_merit, counter):
        nationality_sums = {}  # Sum of weighted ranks per nationality
        nationality_counts = {}  # Total count per nationality

        for nat, rank, count in zip(nationalities, order_of_merit, counter):
            if nat not in nationality_sums:
                nationality_sums[nat] = 0
                nationality_counts[nat] = 0
            nationality_sums[nat] += rank * count  # Weighted rank sum
            nationality_counts[nat] += count       # Total count for this nationality

        # Calculate mean rank for each nationality
        mean_ranks = {
            nat: (nationality_sums[nat] / nationality_counts[nat]) if nationality_counts[nat] > 0 else None
            for nat in nationality_sums
        }

        return mean_ranks
    
    def mean_rank(ages, order_of_merit, counter):
        age_sums = {}  # Sum of weighted ranks per nationality
        age_counts = {}  # Total count per nationality

        for age, rank, count in zip(ages, order_of_merit, counter):
            if age not in age_sums:
                age_sums[age] = 0
                age_counts[age] = 0
            age_sums[age] += rank * count  # Weighted rank sum
            age_counts[age] += count       # Total count for this nationality

        # Calculate mean rank for each nationality
        mean_ranks = {
            nat: (age_sums[nat] / age_counts[nat]) if age_counts[nat] > 0 else None
            for nat in age_sums
        }

        return mean_ranks
    
    # selection of Age-Clusters with own value on X axis  
    age_selection = ['10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70+']
    
    total_age = {'10-20':0, '20-30':0, '30-40':0, '40-50':0, '50-60':0, '60-70':0, '70+':0}

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

        
        for age in age_selection[:len(age_selection)]:
            counter_value = df_players['Age'].value_counts().get(age, 0) # number of players with specific age-cluster
            counter.append(counter_value)
            total_age[age] = total_age[age] + counter_value
            ages.append(age)
            order_of_merit.append(i+1)

    if variant == 0:
        counter = ratio(ages, total_age, counter)

    mean_ranking = mean_rank(ages, order_of_merit, counter)

    # Normalize bubble sizes to prevent overlap
    max_count = max(counter) if counter else 1  # Avoid division by zero
    min_size = 5   # Minimum bubble size
    max_size = 50  # Maximum bubble size
    bubble_sizes = [min_size + (s / max_count) * (max_size - min_size) for s in counter]
    
    # Dynamically adjust chart height based on the number of ranks
    chart_height = max(500, var * 70) 

    # creating figure
    fig = go.Figure()
    colors = px.colors.qualitative.Prism
    colors = colors[:8]
    
    fig.add_trace(go.Scatter(
    x=ages,
    y=order_of_merit,
    mode="markers", 
    marker=dict(
        size=bubble_sizes,  # size of bubble (times two for having bigger bubbles)
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
        template="plotly_white",
        width=800,
        height=chart_height
    )

    return fig, mean_ranking



'''var = 2
fig, mean_ranking = plot_ranking_age(var, 0)
fig.show()
print(mean_ranking)'''