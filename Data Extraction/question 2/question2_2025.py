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

# URL of the events page
url = 'https://app.dartsorakel.com/events'

# Open the webpage
driver.get(url)


# Function to extract the table data from the current page
def extract_table():
    html_content = driver.page_source  # Get the current HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table element
    table = soup.find('table')

    # Define column headers manually
    headers = ["Date", "Tournament", "Category", "Winner", "Winner Avg"]

    # Debugging: Print the extracted headers
    # print("Extracted headers:", headers)

    # Extract all rows (excluding the header row)
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.text.strip() for td in tr.find_all('td')]
        if cells:
            rows.append(cells)

    # Debugging: Print extracted rows
    # print("Extracted rows:", rows)

    return headers, rows


# List to store all extracted data
all_rows = []
headers = None  # Placeholder for table headers

# Maximum number of pages to scrape
max_pages = 5
page_number = 1

# Loop through pages until max_pages is reached
while page_number <= max_pages:
    # Extract table data from the current page
    page_headers, page_rows = extract_table()
    
    # Set headers only once (on the first extraction)
    if headers is None:
        headers = page_headers

    # Append current page's data to the overall list
    all_rows.extend(page_rows)

    # Try clicking the "Next" button to go to the next page
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[text()='2']")
            )  # The button labeled "2" for the next page
        )
        next_button.click()
        page_number += 1  # Increase page count

        # Wait to ensure the new page loads properly
        time.sleep(2)

    except Exception as e:
        print(f"Error clicking 'Next' or no further pages available: {e}")
        break  # Exit the loop if the next page button is unavailable

# Close the WebDriver session
driver.quit()

# Check if data was extracted successfully
if headers and all_rows:
    # Convert extracted data into a Pandas DataFrame
    df = pd.DataFrame(all_rows, columns=headers)

    # Print the first few rows of the DataFrame for verification
    # print(df.head())

    # Save the DataFrame as a CSV file (currently commented out)
    # df.to_csv('Data/question 2/darts_events_all_pages.csv', index=False)
    print("Data successfully extracted and saved as 'darts_events_all_pages.csv'.")
else:
    print("Error: No valid data found to create a DataFrame.")
