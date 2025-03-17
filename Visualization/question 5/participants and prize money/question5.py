import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Funktion zur Umwandlung von Währungsstrings in float
def convert_currency(value):
    if isinstance(value, str):
        value = value.replace('£', '').replace(',', '')
        return float(value)
    return value

# Funktion zur Umwandlung der y-Achsenwerte
def format_y_ticks(value, pos):
    return f'{value / 100000:.0f}'

# CSV-Datei laden
file = 'Data/question 5/question5.csv'
df = pd.read_csv(file)

# Preisgeld-Spalten definieren
columns = ['Champion', 'Runner-up', '3d place', '4d place', 'Quarter finalists', 
           'Last 16', 'Last 24', 'Last 32', 'Last 64', 'Last 96']
labels = ['1st', '2nd', '3rd', '4th', 'Quarter finalists', 'Last 16', 
          'Last 24', 'Last 32', 'Last 64', 'Last 96']

# Daten umwandeln
for column in columns:
    df[column] = df[column].apply(convert_currency)
df['Semi finalists'] = df['Semi finalists'].apply(convert_currency)
df['Total Prize Pool'] = df['Total Prize Pool'].apply(convert_currency)

# Fehlende Werte in allen Preisgeld-Spalten außer "3d place" und "4d place" mit 0 ersetzen
columns_without_3rd_4th = [col for col in columns if col not in ['3d place', '4d place']]
df[columns_without_3rd_4th] = df[columns_without_3rd_4th].fillna(0)

# Spezialfall: 3. und 4. Platz sind manchmal als "Semi Finalists" zusammengefasst
df['3d place'].fillna(df['Semi finalists'], inplace=True)
df['4d place'].fillna(df['Semi finalists'], inplace=True)

# Teilnehmer-Daten gruppieren
participants_per_year = df.groupby('Year')['Participants'].mean()

# Farben definieren
colors = plt.cm.get_cmap("Paired", 10)

# **Diagramm erstellen**
fig, ax1 = plt.subplots(figsize=(10, 6))  # Haupt-Achse für gestapeltes Balkendiagramm

# **Balkendiagramm (Preisgeld)**
bottom_values = 0  # Startwert für Stapel
for i, (column, label) in enumerate(zip(columns, labels)):
    ax1.bar(df['Year'], df[column], bottom=bottom_values, label=label, color=colors(i))
    bottom_values += df[column]  

# Fehlenden Preis auffüllen
missing_prize_money = df['Total Prize Pool'] - bottom_values
ax1.bar(df['Year'], missing_prize_money, bottom=bottom_values, label="Other Prize Money", color='gray', alpha=0.6)

# **Zweite Achse für Teilnehmerzahl**
ax2 = ax1.twinx()  
ax2.plot(participants_per_year.index, participants_per_year.values, marker='o', linestyle='-', color='red', label="Participants")

# Achsenbeschriftung
ax1.set_xlabel("Year")
ax1.set_ylabel("Prize Money in 100.000 £")
ax2.set_ylabel("Participants")

# Y-Achsen Formatierung
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(format_y_ticks))

# **Legendenposition optimieren**
ax1.legend(loc="upper left", fontsize=8, bbox_to_anchor=(1.1, 0.9))
ax2.legend(loc="upper left", fontsize=8, bbox_to_anchor=(1.1, 1), ncol=2)  # Neue Position oberhalb


# Layout optimieren
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.title("Development of Prize Money and Participants over the Years (PDC World Championship)")
plt.tight_layout()

# Diagramm anzeigen
plt.show()
