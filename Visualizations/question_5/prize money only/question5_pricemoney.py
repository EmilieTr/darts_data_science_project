import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# function to convert string currency values into float values
def convert_currency(value):
    if isinstance(value, str):  # is value == string?
        value = value.replace('£', '').replace(',', '')  # remove £ and commas
        return float(value)  # convert into float
    return value  # if value already is a string, directly return

# function for converting y-axis-values
def format_y_ticks(value, pos):
    return f'{value / 100000:.0f}'  # devides through 100.000

# Load CSV file
file = 'Data/question 5/question5.csv'
df = pd.read_csv(file)



# names of prize money columns and the labels we want to have for each column until last 16
#columns = ['Champion', 'Runner-up', '3d place', '4d place', 'Quarter finalists', 'Last 16']
#labels = ['1st', '2nd', '3rd', '4th', 'Quarter fianlists', 'last 16']

# names of prize money columns and the labels we want to have for each column all places
columns = ['Champion', 'Runner-up', '3d place', '4d place', 'Quarter finalists', 'Last 16', 'Last 24', 'Last 32', 'Last 64', 'Last 96']
labels = ['1st', '2nd', '3rd', '4th', 'Quarter fianlists', 'last 16', 'last 24', 'last 32', 'last 64', 'last 96']


# Change prize money data from string to float
for column in columns:
    df[column] = df[column].apply(convert_currency)
df['Semi finalists'] = df['Semi finalists'].apply(convert_currency)
df['Total Prize Pool'] = df['Total Prize Pool'].apply(convert_currency)

# Fehlende Werte in allen Preisgeld-Spalten außer "3d place" und "4d place" mit 0 ersetzen
columns_without_3rd_4th = [col for col in columns if col not in ['3d place', '4d place']]
df[columns_without_3rd_4th] = df[columns_without_3rd_4th].fillna(0)

# special case: in some of the data 3rd and 4th place is summarized into "semi finalsts"
df['3d place'].fillna(df['Semi finalists'], inplace=True)
df['4d place'].fillna(df['Semi finalists'], inplace=True)

# Colors palette
colors = plt.cm.get_cmap("Paired")

plt.figure(figsize=(10, 6))

'''

# line chart:
# Create lines for every position/ placement
for i, (column, label) in enumerate(zip(columns, labels)):
    plt.plot(df['Year'], df[column], marker='', linestyle='-', color=colors(i), label=label)

# axis label & titel
plt.xlabel("Year")
plt.ylabel("Prize Money in £")
plt.title("Development of Prize Money over the Years (PDC World Championship)")
plt.legend(loc="upper left", fontsize=8, bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()
'''

# bar chart
bottom_values = 0  # saves height where new bar begins

for i, (column, label) in enumerate(zip(columns, labels)):
    if bottom_values is None:
        plt.bar(df['Year'], df[column], label=label, color=colors(i))
    else:
        plt.bar(df['Year'], df[column], bottom=bottom_values, label=label, color=colors(i))
        bottom_values += df[column]  # next category comes on top of last bar

# adding up to total prize money
missing_prize_money = df['Total Prize Pool'] - bottom_values
plt.bar(df['Year'], missing_prize_money, bottom=bottom_values, label="Other Prize Money", color='gray', alpha=0.6)

# converting y-axis
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(format_y_ticks))

# Axis labeling & titel
plt.xlabel("Year")
plt.ylabel("Prize Money in 100.000 £")
plt.title("Development of Prize Money over the Years (PDC World Championship)")
plt.legend(loc="upper left", fontsize=8, bbox_to_anchor=(1, 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Horizontale Linien für bessere Lesbarkeit
plt.xticks(rotation=45)  # Jahre besser lesbar machen
plt.tight_layout()

# show diagramm
plt.show()
