import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
import psycopg2

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_connection.Db_Connector import Database_Connector


class DBT:

    def run_model(self, model_file):

        with open(model_file, "r") as f:
            query = f.read()

        conn, cur = None, None
        
        try:
            conn = Database_Connector.get_postgres_connection()
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            print(f"Model executed successfully: {model_file}")

        except Exception as e:
            print(f"Error running model {model_file}: {e}")

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()