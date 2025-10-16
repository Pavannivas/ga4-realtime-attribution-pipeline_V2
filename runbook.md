# 📌 Overview

This runbook describes how to run, monitor, and troubleshoot the Real-Time Attribution Dashboard Project.
It covers ingestion (batch + streaming), dbt models, and the Streamlit dashboard.

---
### ⚠️ Failure Handling & Troubleshooting
---
| **Failure Mode**              | **Symptom**                                          | **Resolution**                                                          |
| ------------------------- | ------------------------------------------------ | ------------------------------------------------------------------- |
| Postgres connection error | `psycopg2.InterfaceError` / "connection refused" | Ensure Postgres is running, check credentials in `Db_Connector.py`. |
| dbt fails to run          | Errors in `run_dbt.py`                           | Verify schema exists, re-run `load_to_postgres.py`, then retry dbt. |
| Dashboard not refreshing  | Streamlit shows stale data                       | Ensure `stream_events.py` is running. Restart dashboard if cached.  |
| Streaming stops           | No new events visible                            | Re-run `stream_events.py` with `--file data/ga4_events.csv`.        |
| Missing tables            | Queries fail in dashboard                        | Run dbt models again: `python run_dbt.py`.                          |


---
## 📊 Monitoring Suggestions

 * Track row counts in ga4_events_raw vs. stg_ga4_events.

 * Add simple logging in stream_events.py to confirm inserts.

 * Streamlit panel shows “live events” → acts as basic real-time monitor.

---
## 💰 Cost Notes

 * This demo runs locally on Postgres → zero infra cost.

 * If deployed on cloud (BigQuery/Postgres on GCP/AWS):

 * Streaming inserts incur cost per row.

 * Dashboard refresh frequency impacts query cost.

 * dbt runs should be scheduled carefully (not too frequent).