import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import re

#list of all major tournaments
major_tournaments = [
    "PDC World Darts Championship",
    "World Matchplay",
    "World Grand Prix (Darts)",
    "Masters of Darts",
    "US Open (Darts)", 
    "Grand Slam of Darts",
    "Players Championship Finals",
    "World Cup of Darts",
    "World Masters (PDC)",
    "World Series of Darts Finals",
    "Champions League of Darts",
]
extra_tournaments = ("European Tour", "Players Championship", "World Series")

#load csv file
file = 'Data/question 2/question2.csv'
df = pd.read_csv(file)
# remove beginning spaces in column names
df.columns = df.columns.str.strip()

#filter data without average and average < 10
df_cleaned = df.dropna(subset=['Average'])
df_cleaned = df_cleaned[df_cleaned['Average'] >= 10]

#filter data of majors end extra tournaments
df_selected = df_cleaned[
    df_cleaned['Tournament'].isin(major_tournaments) | 
    df_cleaned['Tournament'].str.startswith(extra_tournaments, na=False) &
    ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
]



# we don't want to differentiate between the same tournaments with different numbers (Challenge Tour 1, 2, 3 → Challenge Tour)
def normalize_tournament_name(name):
    return re.sub(r'\d+', '', name).strip()  # removes numbers and spaces we don't need

df_selected['Tournament'] = df_selected['Tournament'].apply(normalize_tournament_name)




# change dates into years
df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], errors='coerce')
df_selected['Date'] = pd.to_datetime(df_selected['Date'], errors='coerce')

df_cleaned['Year'] = df_cleaned['Date'].dt.year
df_selected['Year'] = df_selected['Date'].dt.year

# group data by year and calculate the average
average_per_year = df_cleaned.groupby('Year')['Average'].mean()

# Average per tournament and year
df_selected = df_selected[df_selected['Year'] >= 2000] #we only use data beginning in 2000
df_grouped = df_selected.groupby(['Year', 'Tournament'])['Average'].mean().reset_index()




# Colors palette
colors = plt.cm.get_cmap("Paired", len(df_grouped['Tournament'].unique())+1)
length = len(df_grouped['Tournament'].unique())+1

plt.figure(figsize=(12, 6))
'''
# create line chart for average
# deviation because smaller tournaments (with worse average) were not documented earlier
plt.plot(average_per_year.index, average_per_year.values, marker='', linestyle='-', color=colors(1), label='Durchschnittlicher Average')
'''

# create line for every major
unique_tournaments = df_grouped['Tournament'].unique()
for i, tournament in enumerate(unique_tournaments):
    df_tournament = df_grouped[df_grouped['Tournament'] == tournament]
    plt.plot(df_tournament['Year'], df_tournament['Average'], marker='', linestyle='-', color=colors(i), label=tournament)

# create line for total average of majors
avg_all_majors = df_selected.groupby('Year')['Average'].mean()
plt.plot(avg_all_majors.index, avg_all_majors.values, marker='s', linestyle='-', color=colors(length), linewidth=2, label="Average of all majors")




# axis labeling & titel
plt.xlabel("year")
plt.ylabel("average score")
plt.title("Development of average scores over the years")
plt.legend(loc="upper left", fontsize=8, bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()

# show diagramm
plt.show()