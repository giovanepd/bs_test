import requests
import pandas as pd
from datetime import timedelta
from requests.models import PreparedRequest


class APIHandler:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def retrieve_exchange_rates_daily(self, base_currency, start_date, end_date, symbols=None):
        """
        Fetch exchange rates day by day between start_date and end_date using the daily API since the free API limitation.
        Returns a DataFrame containing the data.
        """
        try:
            all_data = []
            current_date = start_date

            while current_date <= end_date:
                formatted_date = current_date.strftime("%Y-%m-%d")
                url = f"{self.api_url}{formatted_date}" 

                params = {
                    "access_key": self.api_key,
                    "base": base_currency,
                }
                if symbols:
                    params["symbols"] = ",".join(symbols)

                req = PreparedRequest()
                req.prepare_url(url, params)

                print(f"Requesting: {req.url}")  # Debug if necessary

                response = requests.get(req.url)
                response.raise_for_status()

                data = response.json()
                if not data.get("success"):
                    raise ValueError(f"API Error: {data.get('error', {}).get('info', 'Unknown error')}")

                rates = data["rates"]
                for currency, rate in rates.items():
                    all_data.append({
                        "base_code": data["base"],
                        "date": formatted_date,
                        "currency_code": currency,
                        "rate": rate
                    })
                    
                current_date += timedelta(days=1)

            if all_data:
                return pd.DataFrame(all_data)
            else:
                print("No data retrieved.")
                return None

        except requests.RequestException as e:
            print(f"Error during API request: {e}")
            return None
        except ValueError as e:
            print(f"Error in API response: {e}")
            return None