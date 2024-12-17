import sqlite3
import os


class DatabaseConnection:
    def __init__(self, db_file):
        self.db_file = db_file

    def connect(self):
        """
        Create and return a SQLite connection
        """
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def setup_database(self):
        """
        Initialize the database structure with required table
        """
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor()

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS exchange_rates (
                    base_code TEXT NOT NULL,
                    date TEXT NOT NULL,
                    rate REAL NOT NULL,
                    currency_code TEXT NOT NULL,
                    PRIMARY KEY (base_code, date,currency_code)
                ) WITHOUT ROWID;
                """)

                conn.commit()
                conn.close()
        except sqlite3.Error as e:
            print(f"Error setting up the database: {e}")
        
    def execute_query(self,query):
        """
        Execute any queries for any purpose
        """
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor()
                for row in cursor.execute(query):
                    print(row)
                conn.close()
        except sqlite3.Error as e:
            print(f"Error setting up the database: {e}")