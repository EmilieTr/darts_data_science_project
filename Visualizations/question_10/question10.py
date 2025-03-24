import pandas as pd
import glob
import os

# Path to the folder containing CSV files
folder_path = "Data/Flashcore/"
output_file = "Visualizations/question_10/180_stats.csv"

# Find all CSV files
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# List for results
results = []

# Process data
for file in csv_files:
    df = pd.read_csv(file)
    
    # Add previous "Leg Value" for each leg
    df["Prev Leg Value"] = df.groupby('Leg')['Leg Value'].shift(1)
    df["Prev Leg Value"].fillna("0-0", inplace=True)
    
    # Split Leg Value into two columns for comparison
    df[["Home Score", "Away Score"]] = (
        df["Leg Value"].str.split("-", expand=True).astype(int)
    )
    df[["Prev Home Score", "Prev Away Score"]] = (
        df["Prev Leg Value"].str.split("-", expand=True).astype(int)
    )
    
    # Determine the winner of a leg
    df["Leg Winner"] = df.apply(
        lambda row: "Home" if row["Home Score"] > row["Prev Home Score"] 
        else ("Away" if row["Away Score"] > row["Prev Away Score"] else "Draw"), 
        axis=1
    )
    
    # Create "First" column
    df["First"] = df["Leg"] == 0

    # Filter columns for 180 throws
    df["180 Home"] = df["Throw Home"] == 180
    df["180 Away"] = df["Throw Away"] == 180
    df["180"] = df["180 Home"] | df["180 Away"]
    df["180 Player"] = df.apply(
        lambda row: "Home" if row["180 Home"] 
        else ("Away" if row["180 Away"] else None), 
        axis=1
    )
    
    # Count cases where the first 180 thrower also won the leg
    total_legs_180 = ((df["First"] == True) & (df["180"] == True)).sum()
    wins_after_180 = (
        (df["First"] == True) & 
        (df["180 Player"] == df["Leg Winner"])
    ).sum()
    
    # Calculate probability
    probability = (
        wins_after_180 / total_legs_180 * 100 
        if total_legs_180 > 0 else 0
    )
    
    # Extract tournament name from filename
    tournament_name = os.path.splitext(os.path.basename(file))[0]
    
    # Store results
    results.append([
        tournament_name, 
        total_legs_180, 
        wins_after_180, 
        probability
    ])

# Ergebnisse als DataFrame speichern
results_df = pd.DataFrame(
                results, 
                columns=[
                    "Tournament", 
                    "Total Legs Start with 180", 
                    "Wins After 180 at first throw", 
                    "Probability (%)"
                ]
            )

# Calculate all averages for the tournaments and convert them into percentages
avg_total_legs_180 = round(
    results_df["Total Legs Start with 180"].mean(), 2
)
avg_wins_after_180 = round(
    results_df["Wins After 180 at first throw"].mean(), 2
)
avg_probability = round(results_df["Probability (%)"].mean(), 2)

# Add a row with overall average values
average_row = pd.DataFrame(
    [["Average", avg_total_legs_180, avg_wins_after_180, avg_probability]],
    columns=results_df.columns,
)

# Append the average row to the table
results_df = pd.concat([results_df, average_row], ignore_index=True)

results_df["Tournament"] = (
    results_df["Tournament"].str.replace("_", " ").str.title()
)

# Sort rows alphabetically based on the 'Tournament' column
results_df = results_df.sort_values(by="Tournament")

# Save CSV file
results_df.to_csv(output_file, index=False)

print(f"Results saved in {output_file}")
