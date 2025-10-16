import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
import time
import csv
from database_connection.Db_Connector import Database_Connector



class Streaming:

    def stream_events(self,csv_file,delay=2,batch_size=1000):
        conn, cur = None, None

        try:
            conn = Database_Connector.get_postgres_connection()
            cur = conn.cursor()

            with open(csv_file, "r") as f:
                reader = csv.DictReader(f)
                batch = []

                for i, row in enumerate(reader):
                    if i >= batch_size:
                        break
                # for row in reader:
                    batch.append((
                        row["event_date"],
                        row["event_timestamp"],
                        row["event_name"],
                        row["user_pseudo_id"],
                        row["source"],
                        row["medium"],
                    ))
                if len(batch) >= batch_size:
                    cur.executemany(
                        """
                        INSERT INTO ga4_events 
                        (event_date, event_timestamp, event_name, user_pseudo_id, source, medium)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        batch
                    )
                    conn.commit()
                    time.sleep(delay)

        except Exception as err:
            print("Error during stream_events:", err)

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()