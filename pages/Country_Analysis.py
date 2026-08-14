import pandas as pd
import plotly.express as px
import streamlit as st

from src.helper import country_analysis, load_olympics

st.title("Country Analysis")

df = load_olympics()
years = ["All"] + sorted(df["year"].unique().tolist())
seasons = ["All"] + sorted(df["season"].unique().tolist())

col1, col2 = st.columns(2)
with col1:
    sel_year = st.selectbox("Select Year", years)
with col2:
    sel_season = st.selectbox("Select Season", seasons)

summary = country_analysis(year=sel_year if sel_year != "All" else None, season=sel_season if sel_season != "All" else None)

st.subheader("Country Performance Table")
st.dataframe(summary.head(50), use_container_width=True)

st.subheader("Top Countries by Medals")
if not summary.empty:
    medal_chart = px.bar(
        summary.head(15),
        x="country",
        y="medals",
        color="golds",
        labels={"country": "Country", "medals": "Medals", "golds": "Golds"},
        title="Top Countries by Total Medals",
    )
    st.plotly_chart(medal_chart, use_container_width=True)
else:
    st.write("No country data available for the selected filters.")
