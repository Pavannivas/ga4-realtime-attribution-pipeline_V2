# Architecture — Real-time Attribution Dashboard

This document explains the overall pipeline design, tools used, and table naming conventions.

---

## Components
**1. Data Generation**

 * Script: generate_ga4_data.py

 * Purpose: Create synthetic GA4-like events (user_pseudo_id, 
 event_timestamp, channel, page, etc.)

 * Output: data/ga4_events.csv

**2. Database**

 * System: Postgres (local)

 * Raw table: ga4_events_raw

 * Data is first batch-loaded (load_to_postgres.py), then incrementally streamed (stream_events.py).

**3. dbt Modeling**

* Staging (stg_ga4_events): Clean + cast types, dedupe, standardize columns.

* Intermediate (int_sessions): Sessionize events by user and time window.

* Marts:
  * mart_first_click: Attribution based on first observed channel.

  * mart_last_click: Attribution based on last observed channel.

**4. Streaming Demo**

* Script: stream_events.py

* Behavior: Reads events line-by-line from CSV

* Inserts into ga4_events_raw with configurable delay (--delay)

* Purpose: Mimics real-time ingestion.

**5. Dashboard**

 * Framework: Streamlit

* Panels:

  * First vs Last Click totals

  * 14-day time series

  * Channel breakdown

  * Live panel (streamed events)

---
## Table Naming Conventions

| Layer        | Table Name         | Description                                  |
| ------------ | ------------------ | -------------------------------------------- |
| Raw          | `ga4_events_raw`   | Ingested GA4-style events                    |
| Staging      | `stg_ga4_events`   | Cleaned + deduplicated events                |
| Intermediate | `int_sessions`     | Sessionized data, user-level transformations |
| Mart         | `mart_first_click` | First click attribution results              |
| Mart         | `mart_last_click`  | Last click attribution results               |

---
## Assumptions & Edge Cases

* Lookback window: 14 days

* Identity resolution: by user_pseudo_id

* Tie-breaking:

  * First-click = earliest event timestamp

  * Last-click = latest event timestamp

  * Deduplication: done in staging (stg_ga4_events)

  * Latency: Streaming demo simulates ~1–2 sec/event; real systems may use Kafka/PubSub.

---
## Diagram (ASCII version)

```
CSV (synthetic GA4 data)
        |
        v
  +-------------------+
  | Postgres (raw)    | <- batch load + streaming insert
  +-------------------+
        |
        v
  +-------------------+
  | dbt staging       | (stg_ga4_events)
  +-------------------+
        |
        v
  +-------------------+
  | dbt intermediate  | (int_sessions)
  +-------------------+
        |
        v
  +--------------------------------+
  | dbt marts                      |
  | - mart_first_click             |
  | - mart_last_click              |
  +--------------------------------+
        |
        v
  +---------------------+
  | Streamlit Dashboard |
  +---------------------+
