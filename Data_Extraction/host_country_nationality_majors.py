import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from utils import get_driver

def clean_html(html_content):
    """
    Clean HTML content by removing unwanted quotation marks from rowspan attributes.
    
    Args:
        html_content: Raw HTML content as string
        
    Returns:
        String of cleaned HTML content
    """
    soup = BeautifulSoup(html_content, "html.parser")
    for td in soup.find_all('td', {'rowspan': True}):
        rowspan_value = td['rowspan']
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
    response = requests.get(url)
    cleaned_html = clean_html(response.text)
    df = pd.read_html(cleaned_html, header=1)[tables_number]
    df = df.loc[:, ~df.columns.duplicated()].copy()  # Remove duplicated columns
    return df


def fetch_nationality(driver, winner_element):
    """
    Fetches the nationality of a winner from their Wikipedia page.
    
    Args:
        driver: Selenium WebDriver instance
        winner_element: Selenium WebElement of the winner name cell
    
    Returns:
        Nationality of the winner or 'Unknown'
    """
    try:
        winner_link = winner_element.find_element(By.TAG_NAME, "a").get_attribute("href")
        driver.get(winner_link)
        time.sleep(2)
        nationality = driver.find_element(By.XPATH, "//span[contains(@class, 'mw-page-title-main')]").text.strip()
        driver.back()
        time.sleep(2)
        return nationality
    except Exception:
        return "Unknown"


def extract_data(row, nationalities, driver):
    """
    Extract data for winners and their nationalities from each row.
    
    Args:
        row: Selenium WebElement representing a table row
        nationalities: Dictionary of winners and their nationalities
        driver: Selenium WebDriver instance
    """
    cells = row.find_elements(By.TAG_NAME, "td")

    if len(cells) >= 3:
        span_elements = cells[1].find_elements(By.TAG_NAME, "span")

        if (len(span_elements) > 1 and "mw-image-border" in span_elements[1].get_attribute("class")):
            winner_element = cells[1]
        else:
            winner_element = cells[2]

        winner = winner_element.text.strip()

        # If winner is not already in the dictionary, fetch nationality
        if winner not in nationalities:
            nationality = fetch_nationality(driver, winner_element)
            nationalities[winner] = nationality


def get_tournament_data(tournament, table_number, driver):
    """
    Get the winners and their nationalities for a specific tournament.
    
    Args:
        tournament: Tournament name
        table_number: Index of the table in the Wikipedia page
        driver: Selenium WebDriver instance
    
    Returns:
        DataFrame with winners, nationalities, and tournament name
    """
    df_list = []
    nationalities = {}  # Dictionary to store winners and their nationalities
    
    url = f"https://de.wikipedia.org/wiki/{tournament}"
    df = get_whole_tables(url, table_number)
    
    # Open the Wikipedia page in Selenium WebDriver
    driver.get(url)
    time.sleep(2)
    
    table = driver.find_element(By.XPATH, f"(//table[@class='wikitable'])[{table_number}]")
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Exclude header row

    # Iterate through each row to extract relevant data
    for row in rows:
        extract_data(row, nationalities, driver)

    df['Nationalität'] = df['Sieger'].map(nationalities)
    df['Tournament'] = tournament.replace("_", " ")
    df_list.append(df)
    
    final_df = pd.concat(df_list, ignore_index=True)
    
    return final_df


def main():
    european_tour = [
        "Austrian Darts Championship", "Austrian Darts Open", "Baltic Sea Darts Open", 
        "Belgian Darts Championship", "Belgian Darts Open", "Czech Darts Open",
        "Danish Darts Open", "Dutch Darts Championship", "Dutch Darts Masters", 
        "European Darts Grand Prix", "European Darts Matchplay", "European Darts Open",
        "European Darts Trophy", "Flanders Darts Trophy", "German Darts Championship",
        "German Darts Grand Prix", "German Darts Masters", "German Darts Open",
        "Gibraltar Darts Trophy", "Hungarian Darts Trophy", "International Darts Open", 
        "Swiss Darts Trophy"
    ]
    
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
    
    driver = get_driver()
    
    df_list_european_tour = []
    df_list_majors = []

    for tournament in european_tour:
        table_number = 1 if tournament == "German Darts Masters" else 2
        df = get_tournament_data(tournament, table_number, driver)
        df_list_european_tour.append(df)

    df_european_tour = pd.concat(df_list_european_tour, ignore_index=True)

    for tournament, table_number in majors:
        df = get_tournament_data(tournament, table_number, driver)
        df_list_majors.append(df)

    df_majors = pd.concat(df_list_majors, ignore_index=True)

    # Save the extracted data to CSV files
    # df_european_tour.to_csv("./Data/host_country_nationality_european_tour.csv", index=False, encoding="utf-8")
    # df_majors.to_csv("./Data/host_country_nationality_majors.csv", index=False, encoding="utf-8")

    print("CSV files have been successfully saved!")

if __name__ == "__main__":
    main()
