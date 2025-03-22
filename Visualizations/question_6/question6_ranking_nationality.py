import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# German to English country names
country_translation = {
    "England": "England",
    "Australien": "Australia",
    "Deutschland": "Germany",
    "Schottland": "Scotland",
    "Niederlande": "Netherlands",
    "Wales": "Wales"
}
country_translation_other = {
    'England': 'England',
    'Australia': 'Australien',
    'Germany': 'Deutschland',
    'Scotland': 'Schottland',
    'Netherlands': 'Niederlande',
    'Wales': 'Wales',
    'Other': 'Other'
}


def plot_ranking_nationality(var, variant):
    def format_name(name):
        # Convert different name formats into a unified format (all lowercase and "first_name surname")
        if "," in name:
            if ", " in name:
                surname, first_name = name.split(", ", 1)
            else:
                surname, first_name = name.split(",", 1)
            surname = surname.lower()
            first_name = first_name.strip().lower()
            return f"{first_name} {surname}"
        return name.strip().lower()

    def convert_names_to_lowercase(df):
        # Convert all names in the DataFrame to lowercase for consistency
        df['Name'] = df['Name'].str.lower()
        return df

    #function for using proportions and not absolute numbers
    def ratio(nationalities, total_nationality, counter):
        for i,nation in enumerate(nationalities):
            if total_nationality[country_translation_other[nation]] == 0:
                counter[i] = 0
            else:
                counter[i] = counter[i] / total_nationality[country_translation_other[nation]]
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
    
    # Selection of nationalities in German (used for searching in the CSV file)
    nationalities_selection_de = list(country_translation.keys()) + ["Other"]
    
    total_nationality = {'England':0, 'Australien':0, 'Deutschland':0, 'Schottland':0, 'Niederlande':0, 'Wales':0, 'Other':0}
    
    # Lists for visualization
    nationalities = []
    order_of_merit = []
    counter = []

    # Lists for proper Y-axis visualization
    y_axis_tickvals = []
    y_axis_ticktext = []
    list_other = []

    for i in range(var):
        y_axis_tickvals.append(i + 1)
        y_axis_ticktext.append(str(i + 1))
        
        # List of all players who ranked in a specific position across years 2009 - 2025
        list_player = []
        for year in range(2009, 2025):
            file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'
            df = pd.read_csv(file)
            name = df[df['Aktuelle Position'] == i + 1]['Name'].iloc[0]
            list_player.append(format_name(name))
        
        # Load player nationality data
        file_players = 'Data/question 6/male_players.csv'
        df = pd.read_csv(file_players)
        df = convert_names_to_lowercase(df)
        df_players = pd.DataFrame(columns=['Name', 'Nationality'])
        
        # Extract nationalities of players
        for player in list_player:
            filtered = df.loc[df['Name'] == player, 'Nationality']
            if not filtered.empty:
                nationality = filtered.iloc[0]
                df_players.loc[len(df_players)] = [player, nationality]
            else:
                print(f"Player {player} not found!")

        total = 0
        for country_de in nationalities_selection_de[:-1]:
            # Count the number of players per nationality
            counter_value = df_players['Nationality'].value_counts().get(country_de, 0)
            counter.append(counter_value)
            total_nationality[country_de] = total_nationality[country_de] + counter_value
            nationalities.append(country_translation.get(country_de, "Other"))
            total += counter_value
            order_of_merit.append(i + 1)

        # Count remaining players as "Other"
        counter.append(len(df_players) - total)
        total_nationality['Other'] = total_nationality['Other'] + (len(df_players)-total)
        nationalities.append("Other")
        order_of_merit.append(i + 1)

        # Collect data for "Other" category
        other = df_players[~df_players['Nationality'].isin(nationalities_selection_de)]
        if not other.empty:
            list_other.append(other['Nationality'].iloc[0])
        else:
            list_other.append(None)

    title = "Absolute Number of nationality to rankings"

    if variant == 0:
        counter = ratio(nationalities, total_nationality, counter)
        title = "Correlation of nationality to rankings"

    mean_ranking = mean_rank(nationalities, order_of_merit, counter)

    # Normalize bubble sizes to prevent overlap
    max_count = max(counter) if counter else 1  # Avoid division by zero
    min_size = 5   # Minimum bubble size
    max_size = 50  # Maximum bubble size
    bubble_sizes = [min_size + (s / max_count) * (max_size - min_size) for s in counter]
    
    # Dynamically adjust chart height based on the number of ranks
    chart_height = min(max(500, var * 70), 2500)

    # Create the plot
    fig = go.Figure()
    colors = px.colors.qualitative.Prism
    colors = colors[:8]
    
    fig.add_trace(go.Scatter(
        x=nationalities,
        y=order_of_merit,
        mode="markers", 
        marker=dict(
            size=bubble_sizes,  # Size of bubble (times two for having bigger bubbles)
            color=counter,  # Color gradient based on number saved in list counter
            colorscale=colors,
            showscale=True 
        ),
        text=[f"Nationality: {nationality}<br>Order of Merit: {rank}<br>Number of Players: {s}" 
            for nationality, rank, s in zip(nationalities, order_of_merit, counter)],  # Custom hover text
    ))

    # Configure layout
    fig.update_layout(
        title=title,
        xaxis_title="Nationality",
        yaxis_title="Order of Merit",
        yaxis_tickformat=".",
        yaxis=dict(tickvals=y_axis_tickvals, ticktext=y_axis_ticktext, showticklabels=True, autorange="reversed"),
        template="plotly_white",
        width=800,
        height=chart_height
    )

    return fig , mean_ranking

'''var = 50

fig, mean_ranking = plot_ranking_nationality(var, 0)
fig.show()
print(mean_ranking)'''