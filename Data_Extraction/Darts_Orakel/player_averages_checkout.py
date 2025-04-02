import os
import sys
import pandas as pd
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import get_driver

from utils_Darts_Orakel import (
    set_date, 
    extract_table, 
    navigate_next_page, 
    get_max_pages, 
    get_stats, 
    set_stat
)


def main():
    # URL of the webpage to scrape
    url = 'https://app.dartsorakel.com/stats/player'
    
    # Initialize WebDriver
    driver = get_driver()
    driver.get(url)

    # Define column headers for the extracted data
    headers = ["Rank", "Player", "Country", "Stat"]
    dfs = []
    page_number = 1

    # Extract all available statistic categories from the dropdown menu
    stats = get_stats(driver)
    stats = stats[0:1]  # Currently limited to the first statistic for testing

    # Define the years to be analyzed
    years = [1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
             2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 
             2022, 2023, 2024]

    previous_stat = 'Functional doubles pcnt'

    # Iterate over all statistics and years
    for stat in stats:
        for year in years:
            year = str(year)

            # Set the date range to the full year
            set_date(driver, "dateTo", f"{year}-12-31")
            set_date(driver, "dateFrom", f"{year}-01-01")

            # Reset selection by choosing the previous statistic first
            set_stat(driver, previous_stat)
            # Now select the desired statistic
            set_stat(driver, stat)

            # Wait for the page to update with new data
            time.sleep(2)

            # Determine the number of available pages
            max_pages = get_max_pages(driver)

            # Loop through pages of data
            while page_number <= max_pages:
                # Extract table data from the current page
                page_rows = extract_table(driver)
                page_number += 1

                if page_rows:
                    # Convert extracted data to a DataFrame
                    df = pd.DataFrame(page_rows, columns=headers)
                    df["Stat Category"] = stat
                    df["Year"] = year
                    dfs.append(df)
                
                # Navigate to the next page
                if not navigate_next_page(driver, page_number):
                    break

        # Update previous_stat after each iteration
        previous_stat = stat

        # Combine all DataFrames into one
        if dfs:
            df_combined = pd.concat(dfs, ignore_index=True)
            save_path = f'./Data/darts_orakel_stats/player_{stat}.csv'
            df_combined.to_csv(save_path, index=False)

    # Close the browser session
    driver.quit()
    print("Data successfully extracted and saved.")

if __name__ == "__main__":
    main()
