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
url = 'https://app.dartsorakel.com/stats/double'

# Open the webpage
driver.get(url)


# Function to set the start date for filtering data
def set_date():
    date = driver.find_element(By.XPATH, "//input[@name='dateFrom']")
    
    # Use JavaScript to set the date field value
    new_date = "1994-01-01"
    driver.execute_script("arguments[0].value = arguments[1];", date, new_date)

    # Trigger an event (some websites detect changes only after an event is fired)
    driver.execute_script(
        "arguments[0].dispatchEvent(new Event('change'));", 
        date
    )
    
    # Wait for the page to load with the new data
    time.sleep(2)


# Function to extract the table from the current page
def extract_table():
    html_content = driver.page_source  # Get the page's HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Locate the table element
    table = soup.find('table')

    # Define column headers manually
    headers = [
        "Rank", "Player", "Country", "Hit", 
        "Single", "Outside", "Other", "Pcnt"
    ]

    # Extract rows from the table
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.text.strip() for td in tr.find_all('td')]
        if cells:
            rows.append(cells)

    return headers, rows


# Function to extract available doubles from the dropdown menu
def get_doubles():
    doubles = []
    dropdown = driver.find_element(By.XPATH, "//select[@name='doubleKey']")
    options = dropdown.find_elements(By.TAG_NAME, 'option')
    
    # Extract text (double values) from each option
    for option in options:
        doubles.append(option.text.strip())
    
    return doubles


# List to store extracted DataFrames
dfs = []
headers = None  # Placeholder for table headers

# Maximum number of pages to scrape per double type
max_pages = 9

# Extract available doubles from the dropdown
doubles = get_doubles()

# Set the date filter
set_date()

# Iterate through each double type and extract data
for double in doubles:
    # Select the double type from the dropdown
    dropdown = driver.find_element(By.XPATH, "//select[@name='doubleKey']")
    dropdown.click()  # Open the dropdown menu
    time.sleep(2)  # Short delay to ensure options are displayed
    doubles_option = driver.find_element(
        By.XPATH, 
        f"//select[@name='doubleKey']/option[text()='{double}']"
    )
    doubles_option.click()  # Select the specific double type

    # Wait for the new data to load
    time.sleep(2)

    # Start from the first page for the selected double type
    page_number = 1

    while page_number <= max_pages:
        # Extract table data from the current page
        page_headers, page_rows = extract_table()

        # Set headers only once (from the first extraction)
        if headers is None:
            headers = page_headers

        # Convert extracted rows to a DataFrame
        df = pd.DataFrame(page_rows, columns=headers)
        df["Double"] = double  # Add a column to indicate the double type
        dfs.append(df)  # Append the DataFrame to the list
        
        # Print extracted data for debugging
        # print(df)
    
        # Try clicking the "Next" button to go to the next page
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[text()='" + str(page_number + 1) + "']")
                )  # Next page button
            )

            # Click the next button only if it's available
            if next_button.is_enabled():
                next_button.click()
                page_number += 1
                time.sleep(2)  # Allow time for the page to load

        except Exception:
            break  # Stop if there are no more pages to navigate

# Close the WebDriver session
driver.quit()

# Combine all DataFrames vertically (row-wise)
# `ignore_index=True` resets the index
df_combined = pd.concat(dfs, ignore_index=True)

# Save the extracted data to a CSV file (currently commented out)
# df_combined.to_csv(r'./Data/question 4/question4.csv', index=False)
print("Data successfully extracted and saved in './Data/question4.csv'.")
