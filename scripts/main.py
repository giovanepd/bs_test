import os
import argparse
from dotenv import load_dotenv
from datetime import datetime, timedelta

from api_handler import APIHandler
from exchange_rate import ExchangeRates
from db_connection import DatabaseConnection

# Load environment variables
load_dotenv()

# Constants
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("FIXER_API_KEY")
DB_FILE = os.getenv("DB_FILE", "exchange_rates.db")

def main():
    parser = argparse.ArgumentParser(description="Exchange Rate Fetcher and Analyzer")
    parser.add_argument("--base_currency", type=str, default="EUR", help="Base currency (e.g., EUR, USD)")
    parser.add_argument("--fetch_from", type=str, help="Data from where we should get our 2 years of data (YYYY-MM-DD)")
    parser.add_argument("--fetch_and_store", action="store_true", help="Fetch and store exchange rate data")
    parser.add_argument("--print_avg", action="store_true", help="Display the average exchange rate")
    parser.add_argument("--currency_avg", type=str, help="Desired currency to calculate the average (e.g., USD)")
    parser.add_argument("--start_date", type=str, help="Start date for data or average calculation (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, help="End date for data or average calculation (YYYY-MM-DD)")

    args = parser.parse_args()

    # Initialize components
    api_handler = APIHandler(API_URL, API_KEY)
    db = DatabaseConnection(DB_FILE)
    fetcher = ExchangeRates(db)
    

    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    if args.start_date:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    else:
        start_date = end_date - timedelta(days=-1)  # Default: 2 days

    # Handle fetch and store
    if args.fetch_and_store:
        if args.base_currency and args.end_date:
            end_date_string = end_date.strftime("%Y-%m-%d")
            start_date_string = start_date.strftime("%Y-%m-%d")
            print(f"Getting data from API - start date {start_date_string} - end date: {end_date_string}")
            df_rates = api_handler.retrieve_exchange_rates_daily(args.base_currency, start_date, end_date)
            if df_rates is not None:
                print("Retrieved data:")
                print(df_rates)
                fetcher.store_data(df_rates)
        else:
            print("Its necessary to have the base_currency and end_date parameters to run the fetch - the start_date is optional")

    # Handle pretty print
    if args.print_avg and args.currency_avg and args.start_date and args.end_date:
        fetcher.pretty_print_average_rate(args.currency_avg, args.start_date, args.end_date)
        #db.execute_query("select * from exchange_rates;")



if __name__ == "__main__":
    main()