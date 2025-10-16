## 📊 Real-Time Attribution Project

End-to-end real-time GA4 attribution pipeline using **BigQuery + dbt + Streamlit** — featuring streaming ingestion, attribution modeling, and live dashboards.

---

## 📌 Features
- **Data ingestion**: Generates synthetic GA4-like events and loads them into Postgres.
- **dbt transformations**:
  - `stg_` → staging models
  - `int_` → intermediate sessionization
  - `mart_` → attribution marts (first_click, last_click)
- **Streaming demo**: Streams events row-by-row from a CSV into Postgres (`stream_events.py`).
- **Dashboard**: Streamlit app with:
  - First vs Last Click totals
  - 14-day time series
  - Channel breakdown
  - Live streaming events panel

---


## 🗂️ Directory Structure

```
real_time_attribution_project
├── data/                         # Data files, generated CSVs
├── dbt_project/                  # DBT models and configurations
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_ga4_events.txt
│   │   ├── intermediate/
│   │   │   └── int_sessions.txt
│   │   └── marts/
│   │       ├── mart_first_click.txt
│   │       └── mart_last_click.txt
│   └── run_dbt.py
├── generate_load_data/           # Data generation & loading scripts
│   ├── generate_ga4_data.py
│   └── load_to_postgres.py
├── scripts/                      # Orchestration scripts (main.py)
├── streaming/                    # Streaming ingestion scripts
│   └── stream_events.py
├── streamlit_app/                # Streamlit dashboard app
│   └── app.py
└── database_connection/          # Database connection helpers
    └── Db_Connector.py
```

**🧹Note on Repo Hygiene**
> - Python cache directories (`__pycache__/`) are excluded via `.gitignore`.  
> - Local data files (`data/*.csv`) are ignored to keep the repo lightweight.  
> - Only reproducible source code, dbt models, and scripts are versioned.  
---

## ⚙️Components Overview


|  **Component**              | **Purpose**                                                         |
| ---------------------- | --------------------------------------------------------------- |
| `generate_ga4_data.py` | Simulates GA4-style user event data.                            |
| `load_to_postgres.py`  | Loads synthetic data into PostgreSQL.                           |
| `stream_events.py`     | Streams event rows into the DB to simulate real-time ingestion. |
| `dbt_project/`         | DBT transformations (staging → intermediate → marts).           |
| `streamlit_app/app.py` | Streamlit dashboard displaying attribution models and trends.   |
| `scripts/main.py`      | Orchestration script to run the full pipeline.                  |


## 🚀 How to Run


**Prerequisites**:
```
    * Python 3.9+
    * PostgreSQL running and accessible
    * DBT installed
    * Virtual environment (optional but recommended)

```
---
**1. ✅ Setup Environment**
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
---
**2. 🏗️ Run the Pipeline** 

You can run everything end-to-end using:
```bash
python scripts/main.py
```

This will:

    - Load them into PostgreSQL

    - Run DBT transformations

    - Start streaming events

    - Launch the Streamlit dashboard

---
**3. 📊 Launch the Dashboard**

You can also launch the dashboard manually:
```bash
streamlit run streamlit_app/app.py
```
---
**🧠 Attribution Models Implemented**

* First Click Attribution
  - Attributes the conversion to the first touchpoint (channel).

* Last Click Attribution
    - Attributes the conversion to the last touchpoint before conversion.

These are calculated via DBT models in marts/

---
**📈 Sample Dashboard**

Once the dashboard is running, visit:
* 🔗 http://localhost:8501

You'll see:

* Attribution comparisons (first vs. last click)

* 14-day conversion trends

* Live streaming events
 
* Channel breakdown charts
---
**🛠️ Technologies Used**

* Python

* PostgreSQL

* DBT

* Streamlit

* Pandas

* psycopg2

* dotenv

---
**📌 TODOs / Enhancements**

* Add unit tests for data generation

* Add Airflow/Dagster for orchestration

* Support additional attribution models (e.g., linear, position-based)

* Kafka integration for real streaming

---
**🧑‍💻 Author**

* Built with ❤️ by A.V.S. PAVAN NIVAS