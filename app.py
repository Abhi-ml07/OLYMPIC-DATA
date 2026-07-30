import streamlit as st
import pandas as pd
from src.helper import load_olympics


def main():
    st.set_page_config(page_title="Olympics Dashboard — Overview", layout="wide")

    st.title("Olympics Data Analysis Dashboard")

    st.markdown(
        """
        **Project Description**

        An interactive Streamlit dashboard that explores historical Olympic data (athletes, events, medals, countries).
        Use the sidebar filters on each page to drill into editions, countries, sports, and gender.
        """
    )

    # Dataset info
    df = load_olympics()
    st.subheader("Dataset Information")
    st.write(f"Rows: {df.shape[0]} — Columns: {df.shape[1]}")
    st.write("Available fields: ", ", ".join(df.columns.tolist()))

    # Technology stack
    st.subheader("Technology Stack")
    st.write("Streamlit, pandas, plotly, Matplotlib, SKlearn, Python")

    # Dashboard features
    st.subheader("Dashboard Features")
    st.markdown(
        """
        - Home: KPIs, trend charts, medal distribution and recent winners
        - Medal Tally: rankings, trends and distributions
        - Country Analysis: country performance and timelines
        - Athlete Analysis: search athletes, profiles and charts
        - Sports Analysis: sport-level stats and heatmaps
        - Gender Analysis: participation and medal split
        - Age Analysis: distributions and boxplots
        - Timeline: edition summaries and trends
        - Records: top medal winners and historical achievements
        """
    )

    # Instructions
    st.subheader("How to run")
    st.code("pip install -r requirements.txt")
    st.code("streamlit run app.py")

    st.markdown("---")
    st.caption("Dataset: athlete_events.csv — Source: Kaggle / curated dataset")


if __name__ == "__main__":
    main()
