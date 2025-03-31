import requests
import pandas as pd
from bs4 import BeautifulSoup

# list for collected data
data = []

# Iterating through years 1994 - 2025 
for year_number in range(1994, 2026):
    year = str(year_number)
    values = {"Year": year}

    # Url of the website, depending on the year
    url = f'https://mastercaller.com/tournaments/pdc-world-championship/{year}'

    # Accessing the website
    response = requests.get(url)
    if response.status_code == 200:
        # Parsing the HTML-Codes
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract number of participants/competitors
        competitors = soup.find(
            'div', 
            {'class': 'col-span-full md:col-span-3 font-medium'}
        )
        while competitors:
            if competitors.text.strip() == "Participants:":
                next_div = competitors.find_next('div')
                if next_div:
                    values["Participants"] = next_div.text.strip()
                break
            competitors = competitors.find_next(
                'div', 
                {'class': 'col-span-full md:col-span-3 font-medium'}
            )

        # Extract the total prize pool
        prize_pool_section = soup.find(
            'span', 
            {'class': 'font-semibold tracking-wider uppercase md:mr-4'}
        )
        if (prize_pool_section and 
                prize_pool_section.text.strip() == "Total Prize Pool"):
            total_prize = prize_pool_section.find_next('span').text.strip()
            values["Total Prize Pool"] = total_prize

        # Extract the prize money for different placements
        def extract_pricemoneys(value):
            price_money = soup.find(
                'div', 
                {'class': 'col-span-5 font-medium'}
            )
            while price_money:
                if price_money.text.strip() == value:
                    next_div = price_money.find_next('div')
                    if next_div:
                        values[value] = next_div.text.strip()
                    return
                price_money = price_money.find_next(
                    'div', 
                    {'class': 'col-span-5 font-medium'}
                )


        # Names of different placements for accessing the table
        table = [
            'Champion', 'Runner-up', 'Semi finalists', '3d place', '4d place', 
            'Quarter finalists', 'Last 16', 'Last 24', 'Last 32', 'Last 64', 
            'Last 96',
        ]
        
        for position in table:
            extract_pricemoneys(position)
        
        # Save values in list "data"
        data.append(values)

    else:  # If website is not found, turn back error message
        print(f"Error for year {year}: {response.status_code}")

# Create a pandas dataframe
df = pd.DataFrame(data)

# Print first 5 lines of the data frame
# print(df.head())

# saving as a csv file
# df.to_csv("./Data/prize_money_participants_wc.csv", index=False)
