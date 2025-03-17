from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time


# Automatically download and use the correct Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the events page
url = 'https://app.dartsorakel.com/events'

# Open the webpage
driver.get(url)


# Function to extract table data from the current page
def extract_table():
    html_content = driver.page_source  # Get the page's HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Locate the table element
    table = soup.find('table')

    # Define column headers manually
    headers = ["Date", "Tournament", "Category", "Winner", "Winner Avg"]

    # Extract rows from the table
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.text.strip() for td in tr.find_all('td')]
        if cells:
            rows.append(cells)

    return headers, rows


# Function to extract available years from the dropdown menu
def get_years():
    years = []
    dropdown = driver.find_element(By.XPATH, "//select[@name='year']")
    options = dropdown.find_elements(By.TAG_NAME, 'option')
    
    # Extract text (year values) from each option
    for option in options:
        years.append(option.text.strip())
    
    return years


# List to store extracted data
all_rows = []
headers = None  # Placeholder for table headers

# Maximum number of pages to scrape per year
max_pages = 13

# Extract available years from the dropdown
years = get_years()

# Iterate through each year to extract data
for year in years:
    # Select the year from the dropdown
    dropdown = driver.find_element(By.XPATH, "//select[@name='year']")
    dropdown.click()  # Open the dropdown menu
    time.sleep(2)  # Short delay to ensure options are displayed
    year_option = driver.find_element(
        By.XPATH, f"//select[@name='year']/option[text()='{year}']")
    year_option.click()  # Select the specific year

    # Wait for the new data to load
    time.sleep(2)

    # Start from the first page for the selected year
    page_number = 1

    while page_number <= max_pages:
        # Extract table data from the current page
        page_headers, page_rows = extract_table()

        # Set headers only once (from the first extraction)
        if headers is None:
            headers = page_headers

        # Append the extracted rows to the overall dataset
        all_rows.extend(page_rows)

        # Try clicking the "Next" button to go to the next page
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//a[text()='{page_number + 1}']")
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

# Check if data was extracted successfully
if headers and all_rows:
    # Convert extracted data into a Pandas DataFrame
    df = pd.DataFrame(all_rows, columns=headers)

    # Print the first few rows for verification
    # print(df.head())

    # Save the DataFrame as a CSV file (currently commented out)
    # df.to_csv(r'./Data/question 2/question2.csv', index=False)
    print("Data successfully extracted and saved in './Data/question2.csv'.")
else:
    print("Error: No valid data found to create the DataFrame.")
