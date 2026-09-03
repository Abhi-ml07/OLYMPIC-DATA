import plotly.express as px
import streamlit as st

from src.helper import load_olympics, timeline

st.title("Timeline")

df = load_olympics()
years = ["All"] + sorted(df["year"].unique().tolist())

sel_year = st.selectbox("Select Year", years)
tl = timeline(year=sel_year if sel_year != "All" else None)

st.subheader("Timeline Table")
st.dataframe(tl, use_container_width=True)

st.subheader("Medal Trend")
if not tl.empty:
    fig = px.line(tl.groupby("year")["medals"].sum().reset_index(), x="year", y="medals", markers=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No medal data for selected filters.")
