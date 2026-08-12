import plotly.express as px
import streamlit as st

from src.helper import athlete_analysis, load_olympics

st.title("Athlete Analysis")

df = load_olympics()
years = ["All"] + sorted(df["year"].unique().tolist())

sel_year = st.selectbox("Select Year", years)
athlete = st.text_input("Search Athlete (partial name)")

results = athlete_analysis(athlete=athlete if athlete else None, year=sel_year if sel_year != "All" else None)

st.subheader("Athlete Performance Table")
st.dataframe(results.head(50), use_container_width=True)

st.subheader("Top Athletes by Medal Count")
if not results.empty:
    chart = px.bar(
        results.head(15),
        x="medals",
        y="name",
        orientation="h",
        color="golds",
        labels={"name": "Athlete", "medals": "Medals", "golds": "Golds"},
        title="Top Athletes by Medal Count",
    )
    st.plotly_chart(chart, use_container_width=True)
else:
    st.write("No athlete data available for the selected filters.")
