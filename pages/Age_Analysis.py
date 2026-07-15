import streamlit as st
import plotly.express as px
import pandas as pd
from src.helper import age_analysis, load_olympics

st.set_page_config(page_title="Age Analysis", layout="wide")
st.title("Age Analysis")

df = load_olympics()
years = ["All"] + sorted(df["year"].unique().tolist())
sports = ["All"] + sorted(df["sport"].unique().tolist())

sel_year = st.selectbox("Select Year", years)
sel_sport = st.selectbox("Select Sport", sports)

filtered = df.copy()
if sel_year != "All":
	filtered = filtered[filtered["year"] == int(sel_year)]
if sel_sport != "All":
	filtered = filtered[filtered["sport"] == sel_sport]

st.subheader("Age Analysis Table")
summary = age_analysis(year=sel_year if sel_year != "All" else None)
st.dataframe(summary.head(200), use_container_width=True)

st.markdown("---")

st.subheader("Age Distribution")
fig_hist = px.histogram(filtered, x="age", nbins=30, title="Age Histogram")
st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Age vs Medal Winners")
medal_df = filtered[filtered["medal"] != "No Medal"]
if not medal_df.empty:
	age_medals = medal_df.groupby("age")["medal"].count().reset_index(name="count")
	fig_med = px.bar(age_medals, x="age", y="count", title="Medal Winners by Age")
	st.plotly_chart(fig_med, use_container_width=True)
else:
	st.write("No medal data for selected filters.")

st.markdown("---")

st.subheader("Average Age by Sport (Top 15)")
avg_age = (
	df.groupby("sport")["age"].mean().reset_index().sort_values("age", ascending=False).head(15)
)
fig_avg = px.bar(avg_age, x="age", y="sport", orientation="h", title="Average Age by Sport")
st.plotly_chart(fig_avg, use_container_width=True)

st.subheader("Boxplot: Age Distribution by Top Sports")
top_sports = df["sport"].value_counts().head(10).index.tolist()
box_df = df[df["sport"].isin(top_sports)]
fig_box = px.box(box_df, x="sport", y="age", points="outliers", title="Age Distribution by Sport")
st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
