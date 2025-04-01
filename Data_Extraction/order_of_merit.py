import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get the table of a specific year
def get_order_of_merit_table(year):
    # URL of the specific year
    url = f"https://www.darts1.de/ranglisten/PDC-Order-of-Merit-{year}.php"

    # Get HTML content
    response = requests.get(url)
    response.encoding = 'utf-8'

    # Check if request is successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all tables on the page
        tables = soup.find_all('table')

        if not tables:
            print(f"No tables found for {year}.")
            return None

        # Find the table with the most rows (target table)
        target_table = max(tables, key=lambda table: len(table.find_all('tr')))
        
        # Extract headers
        headers = []
        header_row = target_table.find_all('tr')[0]
        header_cells = header_row.find_all(['th', 'td'])

        for cell in header_cells:
            headers.append(cell.text.strip())

        # Extract rows, skipping the first one (header row)
        rows = []
        for row in target_table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) == len(headers):  # Ensure row matches header length
                row_data = [cell.text.strip() for cell in cells]
                rows.append(row_data)

        # Return the extracted headers and rows
        return headers, rows

    else:
        print(f"Failed to retrieve data for {year}, status code: {response.status_code}")
        return None


# Function to save data to CSV
def save_to_csv(data, headers, year):
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(f'Data/order_of_merit/order_of_merit_{year}.csv', index=False)
    print(f"Data for {year} saved successfully.")


# Main function to extract data for all years
def main():
    for year in range(2009, 2025):
        year_str = str(year)
        print(f"Processing data for {year_str}...")

        # Get table data for the year
        result = get_order_of_merit_table(year_str)
        
        if result:
            headers, rows = result
            save_to_csv(rows, headers, year_str)


# Execute the main function
if __name__ == "__main__":
    main()
