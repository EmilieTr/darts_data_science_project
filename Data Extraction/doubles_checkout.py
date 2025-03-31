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
url = 'https://app.dartsorakel.com/stats/double'

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


# Function to extract the table data from the current page
def extract_table():
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

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


# Function to extract all available options from the "double" dropdown menu
def get_doubles():
    doubles = []
    dropdown = driver.find_element(By.XPATH, "//select[@name='doubleKey']")
    options = dropdown.find_elements(By.TAG_NAME, 'option')
    for option in options:
        doubles.append(option.text.strip())  # Extract text of each option
    return doubles


# List to store DataFrames
dfs = []

# Maximum number of pages to navigate per selection
max_pages = 6
page_number = 1

# Extract all available double types from the dropdown menu
doubles = get_doubles()

# Define column headers for the extracted data
headers = ["Rank", "Player", "Country", "Hit", "Single", "Outside",
           "Other", "Pcnt"]

# Define the years to be analyzed
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Iterate over all years
for year in years:
    year = str(year)
    
    # Set the date range to the full year
    set_date("dateFrom", year + "-01-01")
    set_date("dateTo", year + "-12-31")

    # Iterate over all double types
    for double in doubles:
        # Select the double type from the dropdown menu
        dropdown = driver.find_element(By.XPATH, "//select[@name='doubleKey']")
        dropdown.click()  # Open the dropdown
        time.sleep(2)  # Short delay to ensure options are visible
        doubles_option = driver.find_element(
            By.XPATH, f"//select[@name='doubleKey']/option[text()='{double}']")
        doubles_option.click()  # Select the option

        # Wait for the page to update with new data
        time.sleep(2)

        # Reset page counter for the current year-double combination
        page_number = 1

        # Loop through pages of data
        while page_number <= max_pages:
            # Extract table data from the current page
            page_rows = extract_table()

            # If no data is available, stop iterating
            if page_rows is None:
                break
            
            # Convert extracted data to a DataFrame
            df = pd.DataFrame(page_rows, columns=headers)
            df["Double"] = double  # Add double type as a column
            df["Year"] = year  # Add year as a column
            dfs.append(df)  # Store the DataFrame
        
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
                    page_number += 1
                    time.sleep(2)  # Wait for the new page to load

            except Exception as e:
                break  # Stop if there is no next page

# Close the browser session
driver.quit()

# Combine all DataFrames into one
df_combined = pd.concat(dfs, ignore_index=True)  # Reset index

# Save the DataFrame as a CSV file (commented out in the original code)
# df_combined.to_csv(r'./Data/doubles_checkout.csv', index=False)

# print("Data successfully extracted and saved in './Data/question1_doubles.csv'.")
