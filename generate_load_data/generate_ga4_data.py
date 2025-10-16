import os
import json
import random
import csv
import time
from datetime import datetime, timedelta



class Generate_GA4_Event:

    def data_generation(self):    
        """
        Generate synthetic GA4-style event data.

        - Simulates 30 days of event logs starting from 2024-08-01.
        - Roughly 35,000 events per day (~1M+ total rows).
        - Events include common user actions: page_view, add_to_cart, purchase, session_start.
        - Each event is associated with a random user and source/medium combination.

        Returns:
            list of lists: Each sublist contains data for a single event.
        """

        users = [f"user_{i}" for i in range(1, 50001)] 
        events = ["page_view", "add_to_cart", "purchase", "session_start"]
        sources = ["google", "facebook", "instagram", "email", "direct"]
        mediums = ["cpc", "organic", "referral", "email", "none"]

        rows = []
        start_date = datetime(2025, 9, 1)
        num_days = 30

        for day in range(num_days):
            date = start_date + timedelta(days=day)
            for _ in range(35000):
                user = random.choice(users)
                event = random.choice(events)
                source = random.choice(sources)
                medium = random.choice(mediums)
                ts = int(time.mktime(date.timetuple())) + random.randint(0, 86400)

                rows.append([
                    date.strftime("%Y%m%d"), 
                    ts,
                    event,
                    user,
                    source,
                    medium
                ])

        return rows  
    
    def convert_to_csv(self,outputPath, rows):
        
        """
        Write synthetic data to a CSV file in the specified path.

        Parameters:
            outputPath (str): Path to save the CSV file.
            rows (list): Generated data to write.

        Returns:
            None. Writes directly to file.
        """

        try:
            with open(outputPath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["event_date","event_timestamp","event_name","user_pseudo_id","source","medium"])
                writer.writerows(rows)
                print(f"Data successfully written to: {outputPath}")

        except Exception as err:
            print("Error at writing to csv :", err)
