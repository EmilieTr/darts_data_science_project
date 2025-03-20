import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Mapping from German to English country names
country_translation = {
    "England": "England",
    "Australien": "Australia",
    "Deutschland": "Germany",
    "Schottland": "Scotland",
    "Niederlande": "Netherlands",
    "Wales": "Wales"
}

def plot_ranking_nationality(var):
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

    # Selection of nationalities in German (used for searching in the CSV file)
    nationalities_selection_de = list(country_translation.keys()) + ["Other"]
    
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
            nationalities.append(country_translation.get(country_de, "Other"))
            total += counter_value
            order_of_merit.append(i + 1)

        # Count remaining players as "Other"
        counter.append(len(df_players) - total)
        nationalities.append("Other")
        order_of_merit.append(i + 1)

        # Collect data for "Other" category
        other = df_players[~df_players['Nationality'].isin(nationalities_selection_de)]
        if not other.empty:
            list_other.append(other['Nationality'].iloc[0])
        else:
            list_other.append(None)

    # Create the plot
    fig = go.Figure()
    colors = px.colors.qualitative.Prism
    
    fig.add_trace(go.Scatter(
        x=nationalities,
        y=order_of_merit,
        mode="markers",
        marker=dict(
            size=[s * 5 for s in counter],  # Adjust bubble size
            color=counter,
            colorscale=colors,
            showscale=True
        ),
        text=[f"Count: {s}" for s in counter],
    ))

    # Configure layout
    fig.update_layout(
        title="Correlation of nationality to rankings",
        xaxis_title="Nationality",
        yaxis_title="Order of Merit",
        yaxis_tickformat=".",
        yaxis=dict(tickvals=y_axis_tickvals, ticktext=y_axis_ticktext, showticklabels=True, autorange="reversed"),
        template="plotly_white",
        width=700,
        height=750
    )

    return fig

var = 10

fig = plot_ranking_nationality(var)
fig.show()