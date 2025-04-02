import os
import sys
import pandas as pd
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import get_driver

from utils_Darts_Orakel import extract_table, navigate_next_page


def main():
    """
    Main function.
    """
    driver = get_driver()

    # URL of the events page
    url = 'https://app.dartsorakel.com/events'

    # Open the webpage
    driver.get(url)

    # List to store all extracted data
    all_rows = []

    # Maximum number of pages to scrape
    max_pages = 5
    page_number = 1
    
    # Define column headers manually
    headers = ["Date", "Tournament", "Category", "Winner", "Winner Avg"]

    # Loop through pages until max_pages is reached
    while page_number <= max_pages:
        # Extract table data from the current page
        page_rows = extract_table(driver)

        # Append current page's data to the overall list
        all_rows.extend(page_rows)

        # Try clicking the "Next" button to go to the next page
        if not navigate_next_page(driver, page_number):
            break

        page_number += 1
        time.sleep(2)

    # Close the WebDriver session
    driver.quit()

    # Check if data was extracted successfully
    if headers and all_rows:
        # Convert extracted data into a Pandas DataFrame
        df = pd.DataFrame(all_rows, columns=headers)

        # Save the DataFrame as a CSV file
        df.to_csv('Data/darts_events_all_pages.csv', index=False)
        print("Data successfully extracted and saved as 'darts_events_all_pages.csv'.")
    else:
        print("Error: No valid data found to create a DataFrame.")


if __name__ == "__main__":
    main()
