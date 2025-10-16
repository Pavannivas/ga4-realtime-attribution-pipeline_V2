import os
import sys
import time
import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_connection.Db_Connector import Database_Connector


class Streamlit_App:

    def run_query(self,query):
        conn = Database_Connector.get_postgres_connection()
        try:
            df = pd.read_sql(query, conn)
        finally:
            conn.close()
        return df

    def Dashboard_Layout(self):
        st.set_page_config(page_title="Real-time Attribution Dashboard", layout="wide")
        st.title("Real-time Attribution Dashboard")

        # Tabs for organization
        tab1, tab2, tab3, tab4 = st.tabs(["First vs Last", "14-Day Trend", "Channel Breakdown", "Live Stream"])

        # ---------------------------
        # First vs Last attribution totals
        # ---------------------------
        with tab1:
            st.subheader("First vs Last Attribution Totals")

            first_click = self.run_query("SELECT channel, COUNT(*) as users FROM mart_first_click GROUP BY channel;")
            last_click = self.run_query("SELECT channel, COUNT(*) as users FROM mart_last_click GROUP BY channel;")

            col1, col2 = st.columns(2)
            with col1:
                st.bar_chart(first_click.set_index("channel"))
            with col2:
                st.bar_chart(last_click.set_index("channel"))

        # ---------------------------
        # 14-day time series
        # ---------------------------
        with tab2:
            st.subheader("14-Day Conversion Trend")

            query = """
            SELECT 
                DATE(TO_TIMESTAMP(last_click_timestamp)) AS event_last_date,
                COUNT(*) AS conversions
            FROM 
                mart_last_click
            WHERE 
                TO_TIMESTAMP(last_click_timestamp) >= NOW() - INTERVAL '14 days'
            GROUP BY 
                event_last_date
            ORDER BY 
                event_last_date;
        """
            trend = self.run_query(query)
            st.line_chart(trend.set_index("event_last_date"))

        # ---------------------------
        # Channel breakdown
        # ---------------------------
        with tab3:
            st.subheader("Channel Breakdown (Last Click)")

            breakdown = self.run_query("""
                SELECT channel, COUNT(*) AS total
                FROM mart_last_click
                GROUP BY channel
                ORDER BY total DESC;
            """)
            st.bar_chart(breakdown.set_index("channel"))

        # ---------------------------
        # Live streamed events
        # ---------------------------
        with tab4:
            st.subheader("Live Events Panel")
            st.caption("Auto-refreshes every 5 seconds")
            st_autorefresh(interval=5 * 1000, key="live_events_refresh")

            live_events = self.run_query("""
                                         SELECT *
                                         FROM stg_ga4_events
                                         ORDER BY event_timestamp DESC
                                         LIMIT 100;
                                        """
                                         )
            st.table(live_events)


if __name__ == "__main__":
    app = Streamlit_App()
    app.Dashboard_Layout()