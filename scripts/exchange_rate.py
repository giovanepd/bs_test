import pandas as pd
import sqlite3
from db_connection import DatabaseConnection


class ExchangeRates:
    def __init__(self, db):
        self.db = db
        self.db.setup_database()

    def store_data(self, data):
        """
        Store exchange rate data into an SQLite database in overwrite mode.
        """
        try:
            conn = self.db.connect()
            if conn:
                df = pd.DataFrame(data)
                
                #Executing like this to be indepotent
                query = """
                INSERT OR REPLACE INTO exchange_rates (base_code, date, currency_code, rate)
                VALUES (?, ?, ?, ?)
                """
                values = df[["base_code", "date", "currency_code", "rate"]].values.tolist()
                
                conn.executemany(query, values)
                conn.commit()
                conn.close()
                #self.db.execute_query("select * from exchange_rates;")
        except Exception as e:
            print(f"Error saving data to database: {e}")

    def calculate_average_rate(self, currency_code, start_date, end_date):
        """
        Calculate the average exchange rate for a given currency over a specified date range.
        """
        try:
            conn = self.db.connect()
            if conn:
                query = f"""
                SELECT AVG(rate) as avg_rate
                FROM exchange_rates
                WHERE currency_code = ?
                  AND date BETWEEN ? AND ?
                """
                result = conn.execute(query, (currency_code, start_date, end_date)).fetchone()
                conn.close()
                return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error calculating average rate: {e}")
            return None

    def pretty_print_average_rate(self, currency_code, start_date, end_date):
        """
        Display the average exchange rate.
        """
        avg_rate = self.calculate_average_rate(currency_code, start_date, end_date)
        if avg_rate:
            print(f"Average exchange rate for {currency_code} from {start_date} to {end_date}: {avg_rate:.4f}")
        else:
            print(f"No data available for {currency_code} from {start_date} to {end_date}.")