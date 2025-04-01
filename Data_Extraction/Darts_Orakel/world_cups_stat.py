import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import get_driver

from utils_Darts_Orakel import extract_table, set_date, get_max_pages, get_stats, set_stat, navigate_next_page


# Main scraping function
def main():
    driver = get_driver()
    url = 'https://app.dartsorakel.com/tournament/stats/1095'
    driver.get(url)

    headers = ["Rank", "Player", "Country", "Stat"]
    dfs = []

    stats = get_stats(driver)
    stats = stats[0:1]  # Limit to a subset of stats (modify as needed)
    years = list(range(2012, 2025))

    previous_stat = 'Functional doubles pcnt'

    # Iterate over all stats and years
    for stat in stats:
        for year in years:
            year_str = str(year)
            set_date("dateTo", f"{year_str}-12-31", driver)
            set_date("dateFrom", f"{year_str}-01-01", driver)
            
            set_stat(previous_stat, driver)  # Keep previous stat for consistency
            set_stat(stat, driver)

            page_number = 1
            max_pages = get_max_pages(driver)
            
            while page_number <= max_pages:
                page_rows = extract_table(driver)
                if page_rows is not None:
                    df = pd.DataFrame(page_rows, columns=headers)
                    df["Stat Category"] = stat
                    df["Year"] = year
                    dfs.append(df)

                    # Navigate to the next page
                    if not navigate_next_page(driver, page_number):
                        break

                    page_number += 1

        previous_stat = stat

        # Combine all DataFrames into one and save to CSV
        if dfs:
            df_combined = pd.concat(dfs, ignore_index=True)
            save_path = f'./Data/darts_orakel_stats/world_cup_{stat}.csv'
            df_combined.to_csv(save_path, index=False)
            print(f"Data successfully saved to {save_path}")

    driver.quit()


# Run the main function
if __name__ == "__main__":
    main()
