import pycountry
import csv

# Define file path
file_path = "Data/question 8/question8.csv"

try:
    # Create and write country codes to CSV file
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Country", "Alpha-3 Code"])  # Column headers
        
        for country in pycountry.countries:
            writer.writerow([country.name, country.alpha_3])

    print(f"CSV file successfully created: {file_path}")

except Exception as e:
    print(f"An error occurred while creating the file: {e}")
