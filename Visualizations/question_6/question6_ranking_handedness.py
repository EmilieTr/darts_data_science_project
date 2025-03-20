import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Mapping from German to English handedness
handedness_translation = {
    "Rechtshänder": "Right-handed",
    "Linkshänder": "Left-handed"
}

def plot_ranking_handedness(var, variant):
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
    def ratio(handedness, total_righthanded, total_lefthanded, counter):
        for i,hand in enumerate(handedness):
            if hand == "Right-handed":
                if total_righthanded == 0:
                    counter[i] = 0
                else:
                    counter[i] = counter[i]/total_righthanded
            elif hand == "Left-handed":
                if total_lefthanded == 0:
                    counter[i] = 0
                else: 
                    counter[i] = counter[i]/total_lefthanded
        return counter
    
    def mean_rank(handedness, order_of_merit, counter):
        right_sum = 0  # Sum of weighted ranks for right-handed players
        left_sum = 0   # Sum of weighted ranks for left-handed players
        right_count = 0  # Total count of right-handed players
        left_count = 0   # Total count of left-handed players

        for hand, rank, count in zip(handedness, order_of_merit, counter):
            if hand == "Right-handed":
                right_sum += rank * count  # Weighted rank
                right_count += count
            elif hand == "Left-handed":
                left_sum += rank * count
                left_count += count

        # Calculate mean ranks (avoid division by zero)
        mean_rank_right = right_sum / right_count if right_count > 0 else None
        mean_rank_left = left_sum / left_count if left_count > 0 else None

        return {'lefthanded':mean_rank_left, 'righthanded': mean_rank_right}

    # Selection of handedness categories in German (used for searching in the CSV file)
    handedness_selection_de = list(handedness_translation.keys())
    
    total_righthanded = 0
    total_lefthanded = 0
    
    # Lists for visualization
    handedness = []
    order_of_merit = []
    counter = []
    
    # Lists for proper Y-axis visualization
    y_axis_tickvals = []
    y_axis_ticktext = []

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
        
        # Load player handedness data
        file_players = 'Data/question 6/male_players.csv'
        df = pd.read_csv(file_players)
        df = convert_names_to_lowercase(df)
        df_players = pd.DataFrame(columns=['Name', 'Handedness'])
        
        # Extract handedness of players
        for player in list_player:
            filtered = df.loc[df['Name'] == player, 'Handedness']
            if not filtered.empty:
                handed = filtered.iloc[0]
                df_players.loc[len(df_players)] = [player, handed]
            else:
                print(f"Player {player} not found!")

        for hand_de in handedness_selection_de:
            # Count the number of players per handedness
            
            counter_value = df_players['Handedness'].value_counts().get(hand_de, 0)
            counter.append(counter_value)
            if hand_de=='Rechtshänder':
                total_righthanded += counter_value
            else: 
                total_lefthanded += counter_value
            handedness.append(handedness_translation.get(hand_de, "Unknown"))
            order_of_merit.append(i + 1)
   

    # if variant is 0 we want the ratios
    if variant == 0:
        counter = ratio(handedness, total_righthanded, total_lefthanded, counter)

    mean_ranking = mean_rank(handedness, order_of_merit, counter)
    print(mean_ranking)

    # Normalize bubble sizes to prevent overlap
    max_count = max(counter) if counter else 1  # Avoid division by zero
    min_size = 5   # Minimum bubble size
    max_size = 50  # Maximum bubble size
    bubble_sizes = [min_size + (s / max_count) * (max_size - min_size) for s in counter]
    
    # Dynamically adjust chart height based on the number of ranks
    chart_height = min(max(500, var * 70), 3000)
    
    # Create the plot
    fig = go.Figure()
    colors = px.colors.qualitative.Prism
    colors = colors[:8]
    
    fig.add_trace(go.Scatter(
        x=handedness,
        y=order_of_merit,
        mode="markers",
        marker=dict(
            size=bubble_sizes,  # Dynamically scaled bubble sizes
            color=counter,
            colorscale=colors,
            showscale=True
        ),
        text=[f"Count: {s}" for s in counter],
    ))

    # Configure layout
    fig.update_layout(
        title="Correlation of handedness to rankings",
        xaxis_title="Handedness",
        yaxis_title="Order of Merit",
        yaxis_tickformat=".",
        yaxis=dict(tickvals=y_axis_tickvals, ticktext=y_axis_ticktext, showticklabels=True, autorange="reversed"),
        template="plotly_white",
        width=800,
        height=chart_height  # Adjusted dynamically
    )

    return fig, mean_ranking

'''var = 10

fig, mean_ranking = plot_ranking_handedness(var, 0)
fig.show()
print(mean_ranking)'''