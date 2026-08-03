import plotly.express as px
import streamlit as st

from src.helper import build_athlete_record_summary, load_olympics

st.title("Records — Top Athletes")
st.caption("Olympic benchmarks for the most decorated, most successful, and most persistent athletes.")

@st.cache_data(show_spinner=False)
def get_record_summary():
    df = load_olympics()
    return build_athlete_record_summary(df)

summary = get_record_summary()

st.subheader("KPIs")
col1, col2, col3 = st.columns(3)
with col1:
    most_decorated = summary.iloc[0] if not summary.empty else None
    if most_decorated is not None:
        st.metric("Most Decorated Athlete", f"{most_decorated['name']} ({int(most_decorated['medals'])} medals)")
    else:
        st.metric("Most Decorated Athlete", "No data")
with col2:
    most_gold = summary.sort_values(["golds", "medals"], ascending=False).iloc[0] if not summary.empty else None
    if most_gold is not None:
        st.metric("Most Gold Medals", f"{most_gold['name']} ({int(most_gold['golds'])} golds)")
    else:
        st.metric("Most Gold Medals", "No data")
with col3:
    most_appearances = summary.sort_values(["appearances", "medals"], ascending=False).iloc[0] if not summary.empty else None
    if most_appearances is not None:
        st.metric("Most Olympic Appearances", f"{most_appearances['name']} ({int(most_appearances['appearances'])})")
    else:
        st.metric("Most Olympic Appearances", "No data")

st.subheader("Tables")
record_table = summary[[
    "name", "country", "medals", "golds", "silvers", "bronzes",
    "appearances", "sports", "years", "oldest_age", "youngest_age",
    "tallest_height", "shortest_height", "heaviest_weight", "lightest_weight"
]].copy()
record_table = record_table.rename(columns={
    "name": "Athlete",
    "country": "Country",
    "medals": "Medals",
    "golds": "Golds",
    "silvers": "Silvers",
    "bronzes": "Bronzes",
    "appearances": "Olympic Appearances",
    "sports": "Sports",
    "years": "Years",
    "oldest_age": "Oldest Age",
    "youngest_age": "Youngest Age",
    "tallest_height": "Tallest Height (cm)",
    "shortest_height": "Shortest Height (cm)",
    "heaviest_weight": "Heaviest Weight (kg)",
    "lightest_weight": "Lightest Weight (kg)",
})

st.markdown("### Olympic Records")
st.dataframe(record_table.head(20), use_container_width=True)

historic = record_table.sort_values(["Medals", "Golds"], ascending=False).head(20)
st.markdown("### Historic Achievements")
st.dataframe(historic, use_container_width=True)

st.subheader("Charts")

with st.spinner("Loading charts..."):
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        top_medal_winners = summary.head(20)
        medal_fig = px.bar(
            top_medal_winners,
            x="name",
            y="medals",
            color="country",
            labels={"name": "Athlete", "medals": "Medals"},
            title="Top 20 Medal Winners",
        )
        st.plotly_chart(medal_fig, use_container_width=True)

    with chart_col2:
        gold_fig = px.bar(
            summary.head(20),
            x="name",
            y="golds",
            color="country",
            labels={"name": "Athlete", "golds": "Golds"},
            title="Top Gold Medalists",
        )
        st.plotly_chart(gold_fig, use_container_width=True)

    chart_col3, chart_col4, chart_col5 = st.columns(3)
    with chart_col3:
        tallest = summary.sort_values("tallest_height", ascending=False).head(10)
        tallest_fig = px.bar(
            tallest,
            x="name",
            y="tallest_height",
            color="country",
            labels={"name": "Athlete", "tallest_height": "Tallest Height (cm)"},
            title="Tallest Medalists",
        )
        st.plotly_chart(tallest_fig, use_container_width=True)

    with chart_col4:
        oldest = summary.sort_values("oldest_age", ascending=False).head(10)
        oldest_fig = px.bar(
            oldest,
            x="name",
            y="oldest_age",
            color="country",
            labels={"name": "Athlete", "oldest_age": "Oldest Age"},
            title="Oldest Medalists",
        )
        st.plotly_chart(oldest_fig, use_container_width=True)

    with chart_col5:
        youngest = summary.sort_values("youngest_age", ascending=True).head(10)
        youngest_fig = px.bar(
            youngest,
            x="name",
            y="youngest_age",
            color="country",
            labels={"name": "Athlete", "youngest_age": "Youngest Age"},
            title="Youngest Medalists",
        )
        st.plotly_chart(youngest_fig, use_container_width=True)
