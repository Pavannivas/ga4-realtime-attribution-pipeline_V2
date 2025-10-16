import os
import sys
import json
import random
import csv
import time
from datetime import datetime, timedelta
import subprocess
import signal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_load_data.generate_ga4_data import Generate_GA4_Event
from generate_load_data.load_to_postgres import LoadData_Postgres
from dbt_project.run_dbt import DBT
from streaming.stream_events import Streaming


class RealTimeAttribution:
    def __init__(self,csvPath):
        self.csvSourcePath = csvPath

    def DataGeneration(self):
        
        ga4_data = Generate_GA4_Event()
        
        data = ga4_data.data_generation()
        
        ga4_data.convert_to_csv(outputPath=self.csvSourcePath,rows=data)

    def LoadData(self):
        loader = LoadData_Postgres()
        loader.load_data_postgres(self.csvSourcePath)

    def RunDbt(self):
        
        """
        Runs dbt models in order: staging, intermediate, marts.
        Assumes models are in dbt_project/models/{stage}/ and are .txt files.
        """

        base_model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dbt_project", "models")

        stages = ["staging", "intermediate", "marts"]

        dbt = DBT()
        for stage in stages:
            stage_path = os.path.join(base_model_path, stage)
            if not os.path.isdir(stage_path):
                print(f"Directory not found: {stage_path}")
                continue
            for filename in sorted(os.listdir(stage_path)):
                if filename.endswith('.txt'):
                    model_path = os.path.join(stage_path,filename)
                    print(f"Running model: {model_path}")
                    dbt.run_model(model_path)
    
    def StreamData(self):
        streaming_data = Streaming()
        streaming_data.stream_events(self.csvSourcePath,delay=2)

    def StreamingDashboard(self,delay_seconds=30):

        # Construct absolute path to app.py
        streamlit_script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "streamlit_app",
            "app.py"
        )
        process = subprocess.Popen(["streamlit", "run", streamlit_script])
        
        # Wait for the specified time
        time.sleep(delay_seconds)
        
        # Send SIGTERM to gracefully terminate Streamlit process
        print(f"Killing Streamlit process after {delay_seconds} seconds...")
        os.kill(process.pid, signal.SIGTERM)
        
        # Wait for process to exit
        process.wait()
        print("Streamlit process terminated.")



def main():
    
    """
    Main function to orchestrate data generation and CSV export.
    """

    csvPath = "/Users/apple/Documents/MyProjects/real_time_attribution_project/data/ga4_events.csv"
    
    real_time_attribution_pipeline = RealTimeAttribution(csvPath)
    
    steps = [
        ("Generating synthetic data", real_time_attribution_pipeline.DataGeneration),
        ("Loading data into Postgres", real_time_attribution_pipeline.LoadData),
        ("Running DBT models", real_time_attribution_pipeline.RunDbt),
        ("Streaming data into Postgres", real_time_attribution_pipeline.StreamData),
        ("Launching dashboard", real_time_attribution_pipeline.StreamingDashboard)
    ]

    for step_name, step_func in steps:
        try:
            print(f"Starting: {step_name}")
            step_func()
            print(f"Completed: {step_name}")
        except Exception as err:
            print(f"Failed: {step_name}")
            print(f" Error: {err}")
            break

if __name__ == "__main__":
    main()