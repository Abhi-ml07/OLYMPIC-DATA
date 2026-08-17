import plotly.express as px
import streamlit as st

from src.helper import gender_analysis, load_olympics

st.title("Gender Analysis")

df = load_olympics()
years = ["All"] + sorted(df["year"].unique().tolist())

sel_year = st.selectbox("Select Year", years)

summary = gender_analysis(year=sel_year if sel_year != "All" else None)

st.subheader("Gender Performance Table")
st.dataframe(summary, use_container_width=True)

st.subheader("Gender Medal Distribution")
if not summary.empty:
    gender_pie = px.pie(summary, names="sex", values="medals", title="Medals by Gender")
    st.plotly_chart(gender_pie, use_container_width=True)
else:
    st.write("No gender data available for the selected filters.")
