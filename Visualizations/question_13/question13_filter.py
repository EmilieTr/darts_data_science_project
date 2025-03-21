import pandas as pd
import glob
import os

# Path to the folder with CSV files
folder_path = "Data/Flashcore/"  # Replace with your actual folder path

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# List for DataFrames
dfs = []

# Read CSV files and add filename as a column
for file in csv_files:
    df_file = pd.read_csv(file)
    df_file["Filename"] = os.path.basename(file)  # Add filename column
    dfs.append(df_file)

# Combine all DataFrames
combined_df = pd.concat(dfs, ignore_index=True)

df_length = len(combined_df)

df_all_nine = pd.DataFrame(columns=['Leg', 'Leg Value', 'Throw-in', 'Value Home', 'Value Away',
       'Throw Home', 'Throw Away', 'Player Home', 'Player Away'])

index = 0

while index < df_length - 1:
    row1 = combined_df.iloc[[index]]
    row2 = combined_df.iloc[[index + 1]]
    
    df_new_nine = pd.DataFrame(columns=['Leg', 'Leg Value', 'Throw-in', 'Value Home', 'Value Away',
       'Throw Home', 'Throw Away', 'Player Home', 'Player Away'])
    df_new_nine = pd.concat([df_new_nine, row1], ignore_index=True)
    
    while (index < df_length - 2) and (row1.loc[index, 'Leg'] < row2.loc[index + 1, 'Leg']):
        df_new_nine = pd.concat([df_new_nine, row2], ignore_index=True)
        index = index + 1
        row1 = combined_df.iloc[[index]]
        row2 = combined_df.iloc[[index + 1]]
    
    if index == df_length - 2:
        df_new_nine = pd.concat([df_new_nine, row2], ignore_index=True)
    
    value_Throw = df_new_nine.loc[0, 'Throw-in']
    if (len(df_new_nine) == 5 and (value_Throw == "VERLORENER ANWURF Away" or value_Throw == "VERLORENER ANWURF Home")) or len(df_new_nine) == 4:
        df_all_nine = pd.concat([df_all_nine, df_new_nine], ignore_index=True)

    index += 1

print("-----------")
print(df_all_nine.head(10))
df_all_nine.to_csv("Visualizations/question_13/nine_darter.csv")