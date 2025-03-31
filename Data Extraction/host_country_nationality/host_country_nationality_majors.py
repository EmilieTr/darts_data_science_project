import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# List of major PDC darts tournaments and corresponding table numbers on Wikipedia
majors = [
    ("PDC_World_Darts_Championship", 1),
    ("World_Matchplay", 2),
    ("World_Grand_Prix_(Darts)", 1),
    ("Las_Vegas_Desert_Classic", 1),
    ("Masters_of_Darts", 3),
    ("US_Open_(Darts)", 4), 
    ("Grand_Slam_of_Darts", 2),
    ("Players_Championship_Finals", 2),
    ("World_Cup_of_Darts", 1),
    ("World_Masters_(PDC)", 1),
    ("World_Series_of_Darts_Finals", 3),
    ("Champions_League_of_Darts", 2)
]

df_list = []  # List to store extracted DataFrames

# Set up the WebDriver for Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def clean_html(html_content):
    """
    Clean HTML content by removing unwanted quotation marks from rowspan attributes.
    
    Args:
        html_content: Raw HTML content as string
        
    Returns:
        String of cleaned HTML content
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find all 'td' elements with 'rowspan' attribute and remove quotes
    for td in soup.find_all('td', {'rowspan': True}):
        rowspan_value = td['rowspan']
        # Remove unwanted quotation marks
        td['rowspan'] = rowspan_value.replace('"', '') if rowspan_value else '1'
    
    return str(soup)


def get_whole_tables(url, tables_number):
    """
    Extract tables from a Wikipedia page.
    
    Args:
        url: Wikipedia page URL
        tables_number: Index of table to extract
        
    Returns:
        DataFrame containing the extracted table data
    """
    # Get the HTML content of the page
    response = requests.get(url)
    
    # Clean the HTML content
    cleaned_html = clean_html(response.text)
    
    # Extract tables from the Wikipedia page
    df = pd.read_html(cleaned_html, header=1)[tables_number]
    # Remove duplicate columns if any
    df = df.loc[:, ~df.columns.duplicated()].copy()
    
    return df


# Dictionary to store winners and their nationalities
nationalities = {}

# Iterate through each tournament
for tournament, tables_number in majors:
    # Construct the Wikipedia URL for the tournament
    url = "https://de.wikipedia.org/wiki/" + tournament
    
    # Extract the tournament table from Wikipedia
    df = get_whole_tables(url, tables_number)
    
    # Open the Wikipedia page in Selenium WebDriver
    driver.get(url)

    # Wait for the page to fully load
    time.sleep(2)

    # Find the tournament table containing winners and nationalities
    table = driver.find_element(
        By.XPATH, f"(//table[@class='wikitable'])[{tables_number}]"
    )

    # Extract all rows from the table (excluding the header row)
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]

    # Iterate through each row to extract relevant data
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")

        # Ensure the row has enough data columns
        if len(cells) >= 3:
            # Check if the second span inside the second td element has the class
            # "mw-image-border"
            span_elements = cells[1].find_elements(By.TAG_NAME, "span")

            if (len(span_elements) > 1 and 
                    "mw-image-border" in span_elements[1].get_attribute("class")):
                sieger = cells[1]  # Use the second td if it has the class
            else:
                sieger = cells[2]
            
            winner = sieger.text.strip()  # Extract the winner's name

            # If winner is not already in the dictionary, fetch nationality
            if winner not in nationalities:
                try:
                    # Get the link to the winner's Wikipedia page
                    winner_link = sieger.find_element(
                        By.TAG_NAME, "a"
                    ).get_attribute("href")
                    
                    # Open the winner's Wikipedia page
                    driver.get(winner_link)
                    time.sleep(2)
                    
                    # Extract nationality
                    try:
                        nationality = driver.find_element(
                            By.XPATH, "//span[contains(@class, 'mw-page-title-main')]"
                        ).text.strip()
                    except Exception as e:
                        nationality = "Unknown"
                    
                    # Go back to the main tournament page
                    driver.back()
                    time.sleep(2)
                except:
                    nationality = "Unknown"

                nationalities[winner] = nationality  # Store winner and nationality

    # Add nationality column to the DataFrame
    df['Nationalität'] = df['Sieger'].map(nationalities)
    
    # Add tournament name column (replace underscores with spaces for readability)
    df['Tournament'] = tournament.replace("_", " ")
    
    # Append DataFrame to the list
    df_list.append(df)

# Combine all DataFrames into a single DataFrame
final_df = pd.concat(df_list, ignore_index=True)

# Close the browser
driver.quit()

# Save the extracted data to a CSV file (currently commented out)
# final_df.to_csv("./Data/host_country_nationality/host_country_nationality_majors.csv", index=False, encoding="utf-8")

print("CSV file has been successfully saved!")
