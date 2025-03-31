import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Set up WebDriver for Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Target URL (Wikipedia page for PDC World Darts Championship)
url = "https://de.wikipedia.org/wiki/PDC_World_Darts_Championship"

# Open the webpage
driver.get(url)

# Wait for the page to fully load
time.sleep(3)

# Find the table containing winners and their nationalities
table = driver.find_element(By.XPATH, "//table[@class='wikitable']")

# Extract all table rows (excluding the header row)
rows = table.find_elements(By.TAG_NAME, "tr")[1:]

# List to store winner names and their nationalities
winners_and_nationalities = []

# Iterate through each row and extract relevant data
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    
    # Ensure the row contains enough data
    if len(cells) >= 3:
        winner = cells[1].text.strip()  # The winner's name is in the second cell
        
        # Link to the winner's Wikipedia page (winner name is a clickable link)
        try:
            winner_link = cells[1].find_element(
                By.TAG_NAME, "a"
            ).get_attribute("href")
            
            driver.get(winner_link)
            time.sleep(2)
            
            # Extract nationality (assuming it is in the infobox)
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

        #print(winner, nationality)
        winners_and_nationalities.append((winner, nationality))

# Close the browser
driver.quit()

# Create a DataFrame
df = pd.DataFrame(winners_and_nationalities, columns=["Winner", "Nationality"])

# Save to CSV file (currently commented out)
# df.to_csv(
#     "./Data/host_country_nationality/host_country_nationality_player_and_country_wm.csv", 
#     index=False, 
#     encoding="utf-8"
# )

# print("CSV file has been successfully saved!")

