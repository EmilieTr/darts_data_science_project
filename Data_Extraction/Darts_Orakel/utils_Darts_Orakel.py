import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def set_date(driver, date_field, new_date):
    """
    Set a date in the input field using JavaScript.
    """
    date = driver.find_element(By.XPATH, f"//input[@name='{date_field}']")
    driver.execute_script("arguments[0].value = arguments[1];", date, new_date)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", date)
    time.sleep(2)  # Wait for the page to update with new data
    
def get_soup(driver):
    """
    Get the BeautifulSoup object of the current page.
    """
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def extract_table(driver):
    """
    Extract the table data from the current page.
    """
    soup = get_soup(driver)
    table = soup.find('table')
    rows = []
    
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.text.strip() for td in tr.find_all('td')]
        if len(cells) == 1 and cells[0] == "No data available in table":
            return None
        if cells:
            rows.append(cells)
    return rows

def navigate_next_page(driver, page_number):
    """
    Navigate to the next page by clicking the "Next" button.
    """
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[text()='{page_number + 1}']")
            )
        )
        if next_button.is_enabled():
            next_button.click()
            time.sleep(2)
            return True
    except Exception:
        return False
    
# Function to extract available years from the dropdown menu
def get_years(driver):
    years = []
    dropdown = driver.find_element(By.XPATH, "//select[@name='year']")
    options = dropdown.find_elements(By.TAG_NAME, 'option')

    # Extract text (year values) from each option
    for option in options:
        years.append(option.text.strip())

    return years

# Function to select a year from the dropdown
def select_year(driver, year):
    dropdown = driver.find_element(By.XPATH, "//select[@name='year']")
    dropdown.click()  # Open the dropdown menu
    time.sleep(2)  # Short delay to ensure options are displayed
    year_option = driver.find_element(By.XPATH, f"//select[@name='year']/option[text()='{year}']")
    year_option.click()  # Select the specific year
    time.sleep(2)  # Wait for the page to load after selection
    
def get_max_pages(driver):
    """
    Determine the number of pages available for scraping.
    """
    ul = get_soup(driver).find("ul", {"class": "pagination"})
    li_elements = ul.find_all("li")
    
    if len(li_elements) >= 2:
        max_pages = li_elements[-2].text  # Extract the page number
    else:
        max_pages = 1  # Default to 1 if pagination is not found

    return int(max_pages)

# Function to extract the available stats from the dropdown
def get_stats(driver):
    stats = []
    dropdown = driver.find_element(By.XPATH, "//select[@name='rankKey']")
    options = dropdown.find_elements(By.TAG_NAME, 'option')
    for option in options:
        stats.append(option.text.strip())
    return stats


# Function to select a stat from the dropdown
def set_stat(stat, driver):
    dropdown = driver.find_element(By.XPATH, "//select[@name='rankKey']")
    dropdown.click()
    time.sleep(2)
    stat_option = driver.find_element(By.XPATH, f"//select[@name='rankKey']/option[text()='{stat}']")
    stat_option.click()
    time.sleep(2)