import pandas as pd

# CSV-Datei laden
df = pd.read_csv('./Data/Flashcore/european_tour_6.csv')

df_length = len(df)


df_all_nine = pd.DataFrame(columns=['Leg', 'Leg Value', 'Throw-in', 'Value Home', 'Value Away',
       'Throw Home', 'Throw Away', 'Player Home', 'Player Away'])

index = 0


while(index < df_length-1):
    row1 = df.iloc[[index]]
    row2 = df.iloc[[index + 1]]
    
    df_new_nine = pd.DataFrame(columns=['Leg', 'Leg Value', 'Throw-in', 'Value Home', 'Value Away',
       'Throw Home', 'Throw Away', 'Player Home', 'Player Away'])
    df_new_nine = pd.concat([df_new_nine, row1], ignore_index=True)
    
    while((index < df_length-2) and (row1.loc[index, 'Leg'] < row2.loc[index + 1, 'Leg'])):
        df_new_nine = pd.concat([df_new_nine, row2], ignore_index=True)
        index = index + 1
        row1 = df.iloc[[index]]
        row2 = df.iloc[[index + 1]]
    
    if index == df_length - 2:
        df_new_nine = pd.concat([df_new_nine, row2], ignore_index=True)
    
    value_Throw = df_new_nine.loc[0, 'Throw-in']
    if (len(df_new_nine) == 5 and (value_Throw == "VERLORENER ANWURF Away" or value_Throw == "VERLORENER ANWURF Home")) or len(df_new_nine) == 4:
        df_all_nine = pd.concat([df_all_nine, df_new_nine], ignore_index=True)

    index = index + 1


print("-----------")
print(df_all_nine)
