from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time


# Automatically download and use the correct WebDriver for Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the webpage to scrape
url = 'https://app.dartsorakel.com/stats/player'

# Open the page in the Chrome browser
driver.get(url)


# Function to set a date in the input field
def set_date(date_field, new_date):  
    date = driver.find_element(By.XPATH, "//input[@name='" + date_field + "']")
    
    # Use JavaScript to set the date value
    driver.execute_script("arguments[0].value = arguments[1];", date, new_date)

    # Trigger an event to ensure the website recognizes the change
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", date)
    
    # Wait for the page to update with new data
    time.sleep(2)


# Function to get the BeautifulSoup object of the current page
def get_soup():
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


# Function to extract the table data from the current page
def extract_table():
    soup = get_soup()
    
    # Find the table element
    table = soup.find('table')

    # Extract all rows (excluding the header row)
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.text.strip() for td in tr.find_all('td')]
        
        # Check if the table is empty
        if len(cells) == 1 and cells[0] == "No data available in table":
            return None
        
        if cells:
            rows.append(cells)

    return rows


# Function to extract all available statistics categories from the dropdown menu
def get_stats():
    stats = []
    dropdown = driver.find_element(By.XPATH, "//select[@name='rankKey']")
    options = dropdown.find_elements(By.TAG_NAME, 'option')
    for option in options:
        stats.append(option.text.strip())  # Extract text of each option
    return stats


# Function to determine the number of pages available
def get_max_pages():
    # Find the pagination <ul> element
    ul = get_soup().find("ul", {"class": "pagination"})

    # Find all <li> elements within the pagination list
    li_elements = ul.find_all("li")

    # Get the second-last <li> element, which represents the last page number
    if len(li_elements) >= 2:
        max_pages = li_elements[-2].text  # Extract the page number
    else:
        max_pages = 1  # Default to 1 if pagination is not found

    return max_pages


# Function to select a statistic from the dropdown menu
def set_stat(stat):
    dropdown = driver.find_element(By.XPATH, "//select[@name='rankKey']")
    dropdown.click()  # Open the dropdown
    time.sleep(2)  # Short delay to ensure options are visible
    stats_option = driver.find_element(
        By.XPATH, f"//select[@name='rankKey']/option[text()='" + stat + "']")
    stats_option.click()  # Select the option


# List to store DataFrames
dfs = []

# Page counter
page_number = 1

# Extract all available statistic categories from the dropdown menu
stats = get_stats()
stats = stats[0:1]  # Currently limited to the first statistic for testing

# Define column headers for the extracted data
headers = ["Rank", "Player", "Country", "Stat"]

# Define the years to be analyzed
years = [1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 
         2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 
         2022, 2023, 2024]

print(stats)

# Store the last selected statistic to reset dropdown selection
previous_stat = 'Functional doubles pcnt'

# Iterate over all statistics and years
for stat in stats:
    for year in years:
        year = str(year)

        # Set the date range to the full year
        set_date("dateTo", year + "-12-31")
        set_date("dateFrom", year + "-01-01")
        
        # Reset selection by choosing the previous statistic first
        set_stat(previous_stat)
        # Now select the desired statistic
        set_stat(stat)

        # Wait for the page to update with new data
        time.sleep(2)

        # Reset page counter for the current year-statistic combination
        page_number = 1

        # Determine the number of available pages
        max_pages = get_max_pages()
        if max_pages == '':
            continue
        else:
            max_pages = int(max_pages)

        print(max_pages)

        # Loop through pages of data
        while page_number <= max_pages:
            time.sleep(2)
            # Extract table data from the current page
            page_rows = extract_table()
            page_number += 1
            time.sleep(2)

            # If data is available, process it
            if page_rows is not None:
                # Convert extracted data to a DataFrame
                df = pd.DataFrame(page_rows, columns=headers)
                df["Stat Category"] = stat  # Add statistic category as a column
                df["Year"] = year  # Add year as a column
                dfs.append(df)  # Store the DataFrame

                print(df) 
                               
                # Wait until the "Next" button is clickable
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//a[text()='" + str(page_number + 1) + "']")
                        )  # Locate next page button
                    )

                    # If the "Next" button is enabled, click it
                    if next_button.is_enabled():
                        next_button.click()
                        time.sleep(2)  # Wait for the new page to load

                except Exception as e:
                    print(e)
                    continue  # If there is no next page, move on
                
    previous_stat = stat  # Update previous statistic

    # Combine all DataFrames into one
    if dfs:
        df_combined = pd.concat(dfs, ignore_index=True)  # Reset index

        # Define save path
        save_path = './Data/Darts_Orakel_Stats/' + stat + '_new.csv'
        df_combined.to_csv(save_path, index=False)  # Save the DataFrame (currently commented out)

# Close the browser session
driver.quit()

# print("Data successfully extracted and saved in './Data/question1_stats.csv'.")

