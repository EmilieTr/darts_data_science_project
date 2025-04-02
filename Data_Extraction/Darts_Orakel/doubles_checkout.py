import sys
import os
from selenium.webdriver.common.by import By
import pandas as pd
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import get_driver

from utils_Darts_Orakel import set_date, extract_table, navigate_next_page


def get_doubles(driver):
    """
    Extract all available options from the "double" dropdown menu.
    """
    doubles = []
    dropdown = driver.find_element(By.XPATH, "//select[@name='doubleKey']")
    options = dropdown.find_elements(By.TAG_NAME, 'option')
    for option in options:
        doubles.append(option.text.strip())
    return doubles


def main():
    # URL of the webpage to scrape
    url = 'https://app.dartsorakel.com/stats/double'
    
    # Initialize WebDriver
    driver = get_driver()
    driver.get(url)

    # Define column headers for the extracted data
    headers = ["Rank", "Player", "Country", "Hit", "Single", "Outside", "Other", "Pcnt"]
    dfs = []
    max_pages = 6
    years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    # Extract all available double types from the dropdown menu
    doubles = get_doubles(driver)

    # Iterate over all years
    for year in years:
        year = str(year)

        # Set the date range to the full year
        set_date(driver, "dateFrom", f"{year}-01-01")
        set_date(driver, "dateTo", f"{year}-12-31")

        # Iterate over all double types
        for double in doubles:
            # Select the double type from the dropdown menu
            dropdown = driver.find_element(By.XPATH, "//select[@name='doubleKey']")
            dropdown.click()
            time.sleep(2)
            doubles_option = driver.find_element(
                By.XPATH, f"//select[@name='doubleKey']/option[text()='{double}']"
            )
            doubles_option.click()

            # Wait for the page to update with new data
            time.sleep(2)

            # Reset page counter for the current year-double combination
            page_number = 1

            # Loop through pages of data
            while page_number <= max_pages:
                # Extract table data from the current page
                page_rows = extract_table(driver)

                # If no data is available, stop iterating
                if page_rows is None:
                    break

                # Convert extracted data to a DataFrame
                df = pd.DataFrame(page_rows, columns=headers)
                df["Double"] = double  # Add double type as a column
                df["Year"] = year  # Add year as a column
                dfs.append(df)  # Store the DataFrame

                # Navigate to the next page
                if not navigate_next_page(driver, page_number):
                    break
                page_number += 1

    # Close the browser session
    driver.quit()

    # Combine all DataFrames into one
    df_combined = pd.concat(dfs, ignore_index=True)

    # Save the DataFrame as a CSV file
    df_combined.to_csv(r'./Data/Darts_Orakel_Stats/doubles_checkout.csv', index=False)
    print("Data successfully extracted and saved in './Data/Darts_Orakel_Stats/doubles_checkout.csv'.")


if __name__ == "__main__":
    main()
