import os
import sys
import json
import psycopg2
import datetime
from dotenv import load_dotenv

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_connection.Db_Connector import Database_Connector

print(load_dotenv())


class LoadData_Postgres:

    def create_ga4_events_table(self, cur):
        """
        Create the ga4_events table if it doesn't already exist.

        Args:
            cur (psycopg2.cursor): database cursor
        """
        create_table_query = """
            CREATE TABLE IF NOT EXISTS ga4_events (
                event_date VARCHAR,
                event_timestamp BIGINT,
                event_name VARCHAR,
                user_pseudo_id VARCHAR,
                source VARCHAR,
                medium VARCHAR
            );
        """
        cur.execute(create_table_query)

    def load_csv_to_table(self, cur, csv_path):
        """
        Load data from a CSV file into the ga4_events table using COPY command.

        Args:
            cur (psycopg2.cursor): database cursor
            csv_path (str): path to the CSV file

        Raises:
            IOError: if file not found or cannot be read
            psycopg2.Error: if COPY fails
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        with open(csv_path, "r") as f:
            next(f)
            cur.copy_from(f, "ga4_events", sep=",")

    def load_data_postgres(self, csv_path):
        """
        Main orchestrator function to load CSV data into PostgreSQL:
        - Connects to DB
        - Creates table if not exists
        - Loads CSV data into the table
        - Commits and closes connections safely

        Args:
            csv_path (str): path to the CSV file
        """

        conn = None
        cur = None
        try:
            conn = Database_Connector.get_postgres_connection()
            cur = conn.cursor()

            self.create_ga4_events_table(cur)
            conn.commit()
            
            self.load_csv_to_table(cur, csv_path)
            conn.commit()

            print(f"CSV data loaded successfully from '{csv_path}' into ga4_events table")

        except Exception as err:
            print(f"Error loading data into Postgres: {err}")

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()