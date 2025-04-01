import os
import sys
import pandas as pd
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import get_driver

from utils_Darts_Orakel import extract_table, navigate_next_page, get_years, select_year


# Main function to orchestrate the scraping process
def main():
    driver = get_driver()

    # URL of the events page
    url = 'https://app.dartsorakel.com/events'

    # Open the webpage
    driver.get(url)

    # List to store extracted data
    all_rows = []
    
    # Define column headers manually
    headers = ["Date", "Tournament", "Category", "Winner", "Winner Avg"]

    # Maximum number of pages to scrape per year
    max_pages = 13

    # Extract available years from the dropdown
    years = get_years(driver)

    # Iterate through each year to extract data
    for year in years:
        # Select the year from the dropdown
        select_year(driver, year)

        # Start from the first page for the selected year
        page_number = 1

        while page_number <= max_pages:
            # Extract table data from the current page
            page_rows = extract_table(driver)

            # Append the extracted rows to the overall dataset
            all_rows.extend(page_rows)

            # Try clicking the "Next" button to go to the next page
            if not navigate_next_page(driver, page_number):
                break  # Stop if there are no more pages to navigate

            page_number += 1  # Increase page count
            time.sleep(2)  # Allow time for the page to load

    # Close the WebDriver session
    driver.quit()

    # Check if data was extracted successfully
    if headers and all_rows:
        # Convert extracted data into a Pandas DataFrame
        df = pd.DataFrame(all_rows, columns=headers)

        # Save the DataFrame as a CSV file
        df.to_csv(r'./Data/tournaments_averages.csv', index=False)
        print("Data successfully extracted and saved in './Data/tournaments_averages.csv'.")
    else:
        print("Error: No valid data found to create the DataFrame.")


# Run the script by calling the main function
if __name__ == "__main__":
    main()
