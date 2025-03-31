from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Automatically download and use the correct WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the page
url = 'https://app.dartsorakel.com/tournament/stats/1095'

# Open the page
driver.get(url)


def set_date(date_field, new_date):
    date = driver.find_element(
        By.XPATH, "//input[@name='" + date_field + "']")
    
    # JavaScript nutzen, um das Datum zu setzen
    driver.execute_script(
        "arguments[0].value = arguments[1];", date, new_date)

    # Event auslösen, falls nötig
    # Manche Webseiten erkennen Änderungen erst nach einem Event
    driver.execute_script(
        "arguments[0].dispatchEvent(new Event('change'));", date)
    
    # Wait for the page with new data to load
    time.sleep(2)


def get_soup():
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    
    return soup


# Function to extract the table from the current page
def extract_table():
    soup = get_soup()
    # Find the table
    table = soup.find('table')

    # Extract the rows (data)
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.text.strip() for td in tr.find_all('td')]
        
        if len(cells) == 1 and cells[0] == "No data available in table":
            return None
        
        if cells:
            rows.append(cells)

    return rows


# Function to extract available years from the dropdown
def get_stats():
    stats = []
    dropdown = driver.find_element(By.XPATH, "//select[@name='rankKey']")
    options = dropdown.find_elements(By.TAG_NAME, 'option')
    for option in options:
        stats.append(option.text.strip())
    return stats


def get_max_pages():
    # Find <ul> (specify  if there is more than one)
    ul = get_soup().find("ul", {"class": "pagination"})
    
    # Find all <li>-elements in the <ul>
    li_elements = ul.find_all("li")

    # Give second to last <li> if at least two <li>-elements exist
    if len(li_elements) >= 2:
        max_pages = li_elements[-2].text
    else:
        max_pages = 1
        
    return max_pages


def set_stat(stat):
    print(stat)
    dropdown = driver.find_element(By.XPATH, "//select[@name='rankKey']")
    dropdown.click()  # Open the dropdown
    time.sleep(2)  # Short delay to ensure the options are displayed
    stats_option = driver.find_element(
        By.XPATH, f"//select[@name='rankKey']/option[text()='" + stat + "']")
    stats_option.click()
    time.sleep(2)


# List to store all data
dfs = []
page_number = 1 

# Extract available years
stats = get_stats()
stats = stats[0:1]  # + stats[13:17] + stats[len(stats)-1:len(stats)]
print("stats", stats)

# Extract the headers (column names)
headers = ["Rank", "Player", "Country", "Stat"]

years = [
    2012, 2013, 2014, 2015, 2016, 
    2017, 2018, 2019, 2020, 2021, 
    2022, 2023, 2024,
]

print(stats)

previous_stat = 'Functional doubles pcnt'

# Iterate over all years and extract data
for stat in stats:
    for year in years:
        year = str(year)
        set_date("dateTo", year + "-12-31")
        set_date("dateFrom", year + "-01-01")
        
        set_stat(previous_stat)
        # Select the year from the dropdown
        set_stat(stat)

        # Reset page number for the current year
        page_number = 1
        if get_max_pages() == '':
            continue
        else:
            max_pages = int(get_max_pages())

        print(max_pages)

        while page_number <= max_pages:
            # Extract the table from the current page
            page_rows = extract_table()
            page_number += 1

            if page_rows != None:
            
                # Convert to DataFrame
                df = pd.DataFrame(page_rows, columns=headers)
                df["Stat Category"] = stat
                df["Year"] = year
                dfs.append(df)
            
                print(df) 
                
                # Wait for the "Next" button to be clickable
                try:                    
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//a[text()='" + str(page_number + 1) + "']")
                        )
                    )

                    # Check if the "Next" button is available
                    if next_button.is_enabled():
                        next_button.click()
                        time.sleep(2)  # Wait to ensure the page has time to load

                except Exception as e:
                    print(e)
                    continue
                
    previous_stat = stat  
            
    # Combine all DataFrames into a single DataFrame
    if dfs:
        df_combined = pd.concat(dfs, ignore_index=True)
        
        save_path = './Data/Darts_Orakel_Stats/world_cup_' + stat + '.csv'
        df_combined.to_csv(save_path, index=False)

# Close the WebDriver
driver.quit()

# print("Data successfully extracted and saved in './Data/Darts_Orakel_Stats/world_cups_stat.csv'.")

