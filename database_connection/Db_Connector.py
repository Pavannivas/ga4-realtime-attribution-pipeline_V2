import os
import json
from datetime import datetime
from dotenv import load_dotenv
import psycopg2


class Database_Connector():

    def get_postgres_connection():
        """
        Establish and return a connection to the PostgreSQL database using environment variables.
        Returns:
            psycopg2.connection: active connection object
        Raises:
            psycopg2.Error: if connection fails
        """
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        ) 