import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Function to convert names from format "SURNAME, First_name" into "First_name Surname"
def convert_name(name):
    if ", " in name:
        surname, first_name = name.split(", ", 1)  # Divide surname and first name
        surname = surname.capitalize()  # Only the first letter of surname is capitalized
        return f"{first_name} {surname}"
    return name 

# Load CSV files
file_2009 = 'Data/order_of_merit/order_of_merit_year_2009.csv'
file_2024 = 'Data/order_of_merit/order_of_merit_year_2024.csv'
df_2009 = pd.read_csv(file_2009)
df_2024 = pd.read_csv(file_2024)

# Convert player names to correct format
list_2009 = [convert_name(name) for name in df_2009['Name'].head(50)]
list_2024 = [convert_name(name) for name in df_2024['Name'].head(50)]

# Load averages
file_averages = 'Data/Darts_Orakel_Stats/Averages.csv'
df_averages = pd.read_csv(file_averages)

# Convert Stat to float
df_averages['Stat'] = df_averages['Stat'].astype(float)

# Extract data for 2009 and 2024
df_averages_2009 = df_averages[(df_averages['Year'] == 2009) & (df_averages['Player'].isin(list_2009))]
df_averages_2024 = df_averages[(df_averages['Year'] == 2024) & (df_averages['Player'].isin(list_2024))]

# Add Year column
df_averages_2009['Year'] = 2009
df_averages_2024['Year'] = 2024

# Combine both datasets
df_combined = pd.concat([df_averages_2009, df_averages_2024])

# Create X positions for bars
players = df_combined["Player"].unique()  # Unique player names
x_indexes = np.arange(len(players))  # Create numerical indexes for players
width = 0.4  # Width of the bars

# Create figure
fig = go.Figure()

# Add bars for each year
for i, year in enumerate([2009, 2024]):
    subset = df_combined[df_combined["Year"] == year]
    player_positions = [players.tolist().index(player) for player in subset["Player"]]
    
    fig.add_trace(go.Bar(
        x=[players[pos] for pos in player_positions],  # Use player names as x-axis labels
        y=subset["Stat"],
        name=str(year),
        offset=i * width - width / 2,  # Adjust bar positioning
    ))

# Update layout
fig.update_layout(
    title="Development of Averages over the Years",
    xaxis_title="Players",
    yaxis_title="Average",
    barmode='group',  # Group bars by year
    xaxis=dict(tickangle=-45),  # Rotate player names for readability
    legend_title="Year"
)

# Show Plot
fig.show()
