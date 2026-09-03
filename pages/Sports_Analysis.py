import plotly.express as px
import streamlit as st

from src.helper import age_analysis, load_olympics

st.title("Sports Analysis")

df = load_olympics()
years = ["All"] + sorted(df["year"].unique().tolist())

sel_year = st.selectbox("Select Year", years)

summary = age_analysis(year=sel_year if sel_year != "All" else None)

st.subheader("Sport Summary Table")
st.dataframe(summary.head(50), use_container_width=True)

st.subheader("Sports Performance Chart")
if not summary.empty:
    sport_bar = px.bar(
        summary.head(15),
        x="medal_winners",
        y="sport",
        orientation="h",
        color="golds",
        labels={"sport": "Sport", "medal_winners": "Medal Winners", "golds": "Golds"},
        title="Top Sports by Medal Winners",
    )
    st.plotly_chart(sport_bar, use_container_width=True)
else:
    st.write("No sport data available for the selected filters.")
