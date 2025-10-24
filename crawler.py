import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_techcombank_financials():
    """
    Crawls the Techcombank financial highlights page and saves the default data to a CSV file.
    """
    url = "https://techcombank.com/en/investors/financial-information/highlights"
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        tables = pd.read_html(str(soup))
        
        # Heuristic to find the main table: the one with the most data
        if tables:
            main_df = max(tables, key=lambda df: df.size)
            
            output_file = 'techcombank_financial_data_default.csv'
            main_df.to_csv(output_file, index=False)
            
            print(f"Data successfully crawled and saved to {output_file}")
            print("Here is a preview of the data:")
            print(main_df.head())
        else:
            print("No tables were found on the page.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    crawl_techcombank_financials()
