import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


#load csv file
file = 'Data/question 5/question5.csv'
df = pd.read_csv(file)
print(df.head())

# Colors palette
colors = plt.cm.get_cmap("Paired", 10)

plt.figure(figsize=(10, 6))

# group data by year
participants_per_year = df.groupby('Year')['Participants'].mean()

#create line
plt.plot(participants_per_year.index, participants_per_year.values, marker='', linestyle='-', color=colors(0), label='Participants')
#create bars
#plt.bar(participants_per_year.index, participants_per_year.values, color=colors(0), label='Participants')



# axis labeling & titel
plt.xlabel("year")
plt.ylabel("participants")
plt.title("Development of participants over the years")
plt.legend(loc="upper left", fontsize=8, bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()

# show diagramm
plt.show()