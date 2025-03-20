import requests
from bs4 import BeautifulSoup
import pandas as pd

# The website has the rankings for order of merit from the years 2009-2024
for year_number in range(2009, 2025):
    year = str(year_number)

    # URL of website, depending on the year
    url = f"https://www.darts1.de/ranglisten/PDC-Order-of-Merit-{year}.php"

    # Getting html-content
    response = requests.get(url)
    response.encoding = 'utf-8'

    # Checking if request is successful
    if response.status_code == 200:
        # Parsing the html-code
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Every table found in source code
        tables = soup.find_all('table')
        
        # If no table was found
        if not tables:
            print("No tables found on the website.")
        # If table was found
        else:
            # If we found more than one table we need to extract the right one
            # In this case it's the one with the most entries
            target_table = None
            max_rows = 0

            for i, table in enumerate(tables):
                rows = table.find_all('tr')
                
                # Testing if the table has more rows than the current biggest table
                if len(rows) > max_rows:
                    max_rows = len(rows)
                    target_table = table

            if target_table:
                # Extracting headers
                headers = []
                header_row = target_table.find_all('tr')[0]
                header_cells = header_row.find_all(['th', 'td'])
                
                for cell in header_cells:
                    headers.append(cell.text.strip())

                # Extracting the rows of the table (every row except the first one)
                rows = []
                for row in target_table.find_all('tr')[1:]:
                    cells = row.find_all('td')
                    # Check if cells and headers have the same length
                    if len(cells) == len(headers):
                        row_data = []
                        for cell in cells:
                            row_data.append(cell.text.strip())
                        rows.append(row_data)
                
                # Creating data frame
                df = pd.DataFrame(rows, columns=headers)
                
                # Optional: printing the first 5 rows of the table
                # print(df.head())
                
                # Saving data frame as csv file
                # df.to_csv(f'Data/order_of_merit/order_of_merit_year_{year}.csv', index=False)
            else:
                print(f"No table could be found for year {year}.")
    else:
        print(f"Error.")