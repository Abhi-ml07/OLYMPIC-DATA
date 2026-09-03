import streamlit as st
import plotly.express as px
import pandas as pd
from src.helper import medal_tally, load_olympics

st.title("Medal Tally")

df = load_olympics()
years = ["All"] + sorted(df["year"].unique().tolist())
seasons = ["All"] + sorted(df["season"].unique().tolist())

col1, col2, col3 = st.columns(3)
with col1:
    sel_year = st.selectbox("Year", years)
with col2:
    sel_season = st.selectbox("Season", seasons)
with col3:
    sel_country = st.selectbox("Country", ["All"] + sorted(df["country"].unique().tolist()))

year_arg = sel_year if sel_year != "All" else None
season_arg = sel_season if sel_season != "All" else None
country_arg = sel_country if sel_country != "All" else None

tally = medal_tally(year=year_arg, season=season_arg, country=country_arg)

if tally.empty:
    st.write("No medals found for the selected filters.")
else:
    # KPIs for selected filters (top country or selected country)
    st.subheader("Medal Summary")
    if country_arg:
        row = tally.loc[country_arg] if country_arg in tally.index else None
        if row is not None:
            gold = int(row.get("Gold", 0))
            silver = int(row.get("Silver", 0))
            bronze = int(row.get("Bronze", 0))
            total = int(row.get("Total", 0))
        else:
            gold = silver = bronze = total = 0
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Gold", gold)
        k2.metric("Silver", silver)
        k3.metric("Bronze", bronze)
        k4.metric("Total", total)

    st.subheader("Medal Ranking")
    st.dataframe(tally.reset_index().sort_values("Total", ascending=False))

    st.subheader("Medal Distribution")
    dist = tally.sum().drop("Total") if "Total" in tally.columns else tally.sum()
    dist_df = pd.DataFrame({"medal": dist.index, "count": dist.values})
    fig = px.pie(dist_df, names="medal", values="count", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Medal Trend (Year-wise)")
    # prepare trend
    trend = df[df["medal"] != "No Medal"]
    if year_arg:
        trend = trend[trend["year"] == int(year_arg)]
    if season_arg:
        trend = trend[trend["season"] == season_arg]
    trend_by_year = trend.groupby("year")["medal"].count().reset_index()
    if not trend_by_year.empty:
        fig2 = px.line(trend_by_year, x="year", y="medal", labels={"medal": "Medals"}, markers=True)
        st.plotly_chart(fig2, use_container_width=True)

