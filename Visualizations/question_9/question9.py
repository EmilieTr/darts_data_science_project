import pandas as pd
import glob
import os

# Path to the folder containing CSV files
folder_path = "Data/flashcore/"
output_file = "Visualizations/question_9/180_stats.csv"

# Find all CSV files
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# List for results
results = []

# Process data
for file in csv_files:
    df = pd.read_csv(file)
    
    # Filter columns for 180 throws
    df["180_Home"] = df["Throw Home"] == 180
    df["180_Away"] = df["Throw Away"] == 180
    df["180"] = df["180_Home"] | df["180_Away"]
    
    # Count the number of 180 throws
    total_180s = df["180"].sum()
    
    # Count consecutive 180 throws
    consecutive_180s = (df["180"] & df["180"].shift(-1)).sum()
    
    # Calculate probability as a percentage
    probability = (
        round((consecutive_180s / total_180s) * 100, 2) 
        if total_180s > 0 else 0
    )

    # Extract tournament name from filename
    tournament_name = os.path.splitext(os.path.basename(file))[0]
    
    # Store results
    results.append([
        tournament_name, 
        total_180s, 
        consecutive_180s, 
        probability
    ])

# Save results in a DataFrame
results_df = pd.DataFrame(
    results, columns=["Tournament", "Total 180s", 
                      "Consecutive 180s", "Probability (%)"]
    )

# Calculate average values for all tournaments
avg_total_180s = round(results_df["Total 180s"].mean(), 2)
avg_consecutive_180s = round(results_df["Consecutive 180s"].mean(), 2)
avg_probability = round(results_df["Probability (%)"].mean(), 2)

# Add row with total average values
average_row = pd.DataFrame(
    [["Average", avg_total_180s, avg_consecutive_180s, avg_probability]],
    columns=results_df.columns
)

# Append average row to the table
results_df = pd.concat([results_df, average_row], ignore_index=True)

results_df['Tournament'] = (
    results_df['Tournament']
    .str.replace('_', ' ')
    .str.title()
)

# Sort rows alphabetically
results_df = results_df.sort_values(by='Tournament')

# Save CSV file
results_df.to_csv(output_file, index=False)

# print(f"Ergebnisse gespeichert in {output_file}")
