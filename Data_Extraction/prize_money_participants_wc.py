import requests
import pandas as pd
from bs4 import BeautifulSoup

def extract_prize_money(soup, value):
    """Extract the prize money for a specific placement."""
    prize_money_section = soup.find(
        'div', 
        {'class': 'col-span-5 font-medium'}
    )
    while prize_money_section:
        if prize_money_section.text.strip() == value:
            next_div = prize_money_section.find_next('div')
            if next_div:
                return next_div.text.strip()
        prize_money_section = prize_money_section.find_next(
            'div', 
            {'class': 'col-span-5 font-medium'}
        )
    return None

def fetch_world_championship_data(year):
    """Fetch data for a specific year of the PDC World Championship."""
    values = {"Year": str(year)}

    # URL of the website for the tournament year
    url = f'https://mastercaller.com/tournaments/pdc-world-championship/{year}'

    # Accessing the website
    response = requests.get(url)
    if response.status_code == 200:
        # Parsing the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract number of participants
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
        if prize_pool_section and prize_pool_section.text.strip() == "Total Prize Pool":
            total_prize = prize_pool_section.find_next('span').text.strip()
            values["Total Prize Pool"] = total_prize

        # Define prize money placements
        prize_positions = [
            'Champion', 'Runner-up', 'Semi finalists', '3d place', '4d place', 
            'Quarter finalists', 'Last 16', 'Last 24', 'Last 32', 'Last 64', 
            'Last 96',
        ]
        
        # Extract prize money for each placement
        for position in prize_positions:
            prize_money = extract_prize_money(soup, position)
            if prize_money:
                values[position] = prize_money

        return values
    else:  # If the website is not found, return error
        print(f"Error for year {year}: {response.status_code}")
        return None


def main():
    # List for storing all data
    data = []

    # Iterating through years 1994 - 2025
    for year in range(1994, 2026):
        # Fetch data for the year
        values = fetch_world_championship_data(year)
        
        if values:
            # Add the fetched data to the list
            data.append(values)

    # Create a pandas dataframe
    df = pd.DataFrame(data)

    # Print first 5 lines of the dataframe
    # print(df.head())

    # Save the data as a CSV file
    # df.to_csv("./Data/prize_money_participants_wc.csv", index=False)


# Execute the main function
if __name__ == "__main__":
    main()
