import pandas as pd
import plotly.express as px
import streamlit as st

from src.helper import load_olympics, medal_tally

st.set_page_config(page_title="Home", page_icon="🏅", layout="wide")

st.markdown(
    "<div style='display:flex; align-items:center; justify-content:space-between; gap:16px;'>"
    "<div>"
    "<h1 style='margin:0;'>Olympics Dashboard</h1>"
    "<p style='margin:6px 0 0 0; color:#6b7280;'>Explore Olympic history through athletes, countries, medals, and records.</p>"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown("---")

st.title("Home — Overview of Olympic Games")

df = load_olympics()

# Sidebar filters
st.sidebar.header("Filters")
years = ["All"] + sorted(df["year"].unique().tolist())
countries = ["All"] + sorted(df["country"].unique().tolist())
sports = ["All"] + sorted(df["sport"].unique().tolist())
genders = ["All"] + sorted(df["sex"].unique().tolist())

sel_year = st.sidebar.selectbox("Year", years, index=0)
sel_country = st.sidebar.selectbox("Country", countries, index=0)
sel_sport = st.sidebar.selectbox("Sport", sports, index=0)
sel_gender = st.sidebar.selectbox("Gender", genders, index=0)
sel_submmit = st.sidebar.button("Apply Filters")



def apply_filters(df: pd.DataFrame):
    filtered = df.copy()
    if sel_year != "All":
        filtered = filtered[filtered["year"] == int(sel_year)]
    if sel_country != "All":
        filtered = filtered[filtered["country"] == sel_country]
    if sel_sport != "All":
        filtered = filtered[filtered["sport"] == sel_sport]
    if sel_gender != "All":
        filtered = filtered[filtered["sex"] == sel_gender]
    return filtered


filtered = apply_filters(df)

# KPI cards
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Olympic Editions", len(df["year"].unique()))
with col2:
    st.metric("Total Countries", df["country"].nunique())
with col3:
    st.metric("Total Athletes", df["id"].nunique())
with col4:
    st.metric("Total Sports", df["sport"].nunique())
with col5:
    st.metric("Total Events", df["event"].nunique())
with col6:
    st.metric("Total Medals", int((df["medal"] != "No Medal").sum()))

st.markdown("---")

st.subheader("Latest Olympic Edition Summary")
latest_year = df["year"].max()
latest_df = df[df["year"] == latest_year]
summary = {
    "Year": latest_year,
    "Host City": latest_df["city"].mode().iat[0] if not latest_df["city"].mode().empty else "N/A",
    "Athletes": int(latest_df["id"].nunique()),
    "Countries": int(latest_df["country"].nunique()),
    "Events": int(latest_df["event"].nunique()),
    "Sports": int(latest_df["sport"].nunique()),
}
st.table(summary)

st.subheader("Recent Medal Winners (Latest Edition)")
recent = (
    df[df["year"] == df["year"].max()]
    .query("medal != 'No Medal'")
    .groupby("country")["medal"]
    .value_counts()
    .unstack(fill_value=0)
)
if not recent.empty:
    recent["Total"] = recent.sum(axis=1)
    st.dataframe(recent.sort_values("Total", ascending=False).head(10), use_container_width=True)
else:
    st.write("No recent medal data available")

st.markdown("---")

# Charts
r1c1, r1c2 = st.columns([2, 1])

with r1c1:
    st.subheader("Athletes Growth Over Years")
    athletes_by_year = df.groupby("year")["id"].nunique().reset_index()
    fig = px.line(athletes_by_year, x="year", y="id", labels={"id": "Athletes"}, markers=True)
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    st.subheader("Top 10 Countries by Medals")
    tally = medal_tally()
    if not tally.empty:
        top10 = tally.head(10).reset_index()
        bar = px.bar(top10, x="Total", y="country", orientation="h", color="Total", text="Total")
        st.plotly_chart(bar, use_container_width=True)

r2c1, r2c2, r2c3 = st.columns(3)

with r2c1:
    st.subheader("Participating Countries Over Years")
    countries_by_year = df.groupby("year")["country"].nunique().reset_index()
    fig2 = px.line(countries_by_year, x="year", y="country", labels={"country": "Countries"}, markers=True)
    st.plotly_chart(fig2, use_container_width=True)

with r2c2:
    st.subheader("Medal Distribution (Overall)")
    medals = df[df["medal"] != "No Medal"]["medal"].value_counts().reset_index()
    medals.columns = ["medal", "count"]
    fig3 = px.pie(medals, names="medal", values="count", hole=0.4)
    st.plotly_chart(fig3, use_container_width=True)

with r2c3:
    st.subheader("Gender Participation (Overall)")
    gender = df.groupby("sex")["id"].nunique().reset_index()
    fig4 = px.pie(gender, names="sex", values="id", hole=0.4)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Bottom charts and tables
bc1, bc2 = st.columns([2, 1])

with bc1:
    st.subheader("Top Sports by Number of Events")
    top_sports = df.groupby("sport")["event"].nunique().reset_index().sort_values("event", ascending=False).head(10)
    fig5 = px.bar(top_sports, x="event", y="sport", orientation="h", text="event")
    st.plotly_chart(fig5, use_container_width=True)

with bc2:
    st.subheader("Latest Olympic Edition Summary")
    latest_year = df["year"].max()
    latest_df = df[df["year"] == latest_year]
    summary = {
        "Year": latest_year,
        "Host City": latest_df["city"].mode().iat[0] if not latest_df["city"].mode().empty else "N/A",
        "Athletes": int(latest_df["id"].nunique()),
        "Countries": int(latest_df["country"].nunique()),
        "Events": int(latest_df["event"].nunique()),
        "Sports": int(latest_df["sport"].nunique()),
    }
    st.table(summary)

