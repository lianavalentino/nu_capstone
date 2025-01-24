# import subprocess
# import sys

# # Ensure required packages are installed
# required_packages = ['requests', 'beautifulsoup4', 'pandas', 'yfinance']

# for package in required_packages:
#     try:
#         __import__(package)
#     except ImportError:
#         print(f"Package '{package}' not found. Installing...")
#         subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf


# URL of the webpage containing the table
url = "https://www.slickcharts.com/sp500"
request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send an HTTP request to fetch the webpage content
response = requests.get(url, headers=request_headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table within the div with class 'table-responsive'
    table_div = soup.find("div", class_="table-responsive")
    if table_div:
        table = table_div.find("table")
        
        # Extract table headers
        headers = [th.text.strip() for th in table.find("thead").find_all("th")]

        # Extract table rows
        rows = []
        for tr in table.find("tbody").find_all("tr"):
            row = [td.text.strip() for td in tr.find_all("td")]
            rows.append(row)

        # Create a DataFrame
        sp500_df = pd.DataFrame(rows, columns=headers)
        
        sp500_df.to_csv("~/nu_capstone/data/raw/sp500_stocks.csv", index=False)
        print("S&P 500 stocks saved to 'sp500_stocks.csv'")
    else:
        print("Table not found in the specified div.")
else:
    print(f"Failed to fetch webpage. Status code: {response.status_code}")

# Function to get sector for a stock symbol
def get_sector(symbol):
    try:
        stock = yf.Ticker(symbol)
        return stock.info.get("sector", "Unknown")
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return "Unknown"

# Add a new column 'Sector'
sp500_df["Sector"] = sp500_df["Symbol"].apply(get_sector)

# Get the top 50 technology stocks
tech_stocks = sp500_df[sp500_df["Sector"] == "Technology"].iloc[:50]
tech_stocks = tech_stocks[["Company", "Symbol"]].reset_index(drop=True)
tech_stocks.to_csv("~/nu_capstone/data/processed/sp50_tech_stocks.csv", index=False)
print("Top 50 technology stocks saved to 'sp50_tech_stocks.csv'")