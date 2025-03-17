import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# function for converting names from format SURNAME, First_name into format First_name Surname
def convert_name(name):
    if ", " in name:
        surname, first_name = name.split(", ", 1)  # divide surname and first name
        surname = surname.capitalize()  # only first letter of surname is capitalized
        return f"{first_name} {surname}"
    return name 

# Load csv files
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

# Colors palette
colors = plt.cm.get_cmap("Paired")

# Plot
plt.figure(figsize=(12, 6))

# Plot bars for each year
for i, year in enumerate([2009, 2024]):
    subset = df_combined[df_combined["Year"] == year]
    player_positions = [players.tolist().index(player) for player in subset["Player"]]
    plt.bar(
        np.array(player_positions) + i * width, subset["Stat"], width=width, color=colors(i*2), label=f"{year}"
    )

# Labels & Title
plt.xlabel("Players")
plt.ylabel("Average")
plt.title("Development of Averages over the Years")
plt.xticks(x_indexes + width / 2, players, rotation=45, ha="right")  # Rotate names for readability
plt.legend(title="Year")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Show Plot
plt.show()
