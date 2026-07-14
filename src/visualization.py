import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.helper import load_olympics


def bar_chart(year=None, season=None, country=None, n=10):
    df = load_olympics()
    filtered = df.copy()

    if year is not None:
        filtered = filtered[filtered["year"] == int(year)]
    if season is not None and str(season).strip().lower() != "all":
        filtered = filtered[filtered["season"].str.lower() == str(season).strip().lower()]
    if country is not None:
        filtered = filtered[filtered["country"].str.lower() == str(country).strip().lower()]

    medal_df = filtered[filtered["medal"] != "No Medal"]
    if medal_df.empty:
        return go.Figure()

    counts = (
        medal_df.groupby("country")["medal"]
        .value_counts()
        .unstack(fill_value=0)
        .reindex(columns=["Gold", "Silver", "Bronze"], fill_value=0)
    )
    counts["Total"] = counts.sum(axis=1)
    top = counts.sort_values("Total", ascending=False).head(n).reset_index()

    fig = px.bar(
        top,
        x="country",
        y="Total",
        color="country",
        title="Top Countries by Total Medals",
    )
    return fig


def line_chart(year=None, season=None, country=None):
    df = load_olympics()
    filtered = df.copy()

    if year is not None:
        filtered = filtered[filtered["year"] == int(year)]
    if season is not None and str(season).strip().lower() != "all":
        filtered = filtered[filtered["season"].str.lower() == str(season).strip().lower()]
    if country is not None:
        filtered = filtered[filtered["country"].str.lower() == str(country).strip().lower()]

    medal_df = filtered[filtered["medal"] != "No Medal"]
    if medal_df.empty:
        return go.Figure()

    yearly = (
        medal_df.groupby(["year", "country"])
        .size()
        .reset_index(name="medals")
    )
    yearly = yearly.sort_values(["year", "medals"], ascending=[True, False])

    if yearly.empty:
        return go.Figure()

    fig = px.line(
        yearly,
        x="year",
        y="medals",
        color="country",
        markers=True,
        title="Medal Trends Over Time",
    )
    return fig


def pie_chart(year=None, season=None, country=None):
    df = load_olympics()
    filtered = df.copy()

    if year is not None:
        filtered = filtered[filtered["year"] == int(year)]
    if season is not None and str(season).strip().lower() != "all":
        filtered = filtered[filtered["season"].str.lower() == str(season).strip().lower()]
    if country is not None:
        filtered = filtered[filtered["country"].str.lower() == str(country).strip().lower()]

    medal_df = filtered[filtered["medal"] != "No Medal"]
    if medal_df.empty:
        return go.Figure()

    counts = medal_df["medal"].value_counts().reset_index()
    counts.columns = ["medal", "count"]
    fig = px.pie(counts, values="count", names="medal", title="Medal Distribution")
    return fig


def heatmap(year=None, season=None, country=None):
    df = load_olympics()
    filtered = df.copy()

    if year is not None:
        filtered = filtered[filtered["year"] == int(year)]
    if season is not None and str(season).strip().lower() != "all":
        filtered = filtered[filtered["season"].str.lower() == str(season).strip().lower()]
    if country is not None:
        filtered = filtered[filtered["country"].str.lower() == str(country).strip().lower()]

    medal_df = filtered[filtered["medal"] != "No Medal"]
    if medal_df.empty:
        return go.Figure()

    pivot = (
        medal_df.groupby(["country", "sport"])
        .size()
        .reset_index(name="medals")
        .pivot(index="country", columns="sport", values="medals")
        .fillna(0)
    )
    fig = px.imshow(pivot, title="Medals by Country and Sport", aspect="auto")
    return fig


def histogram(year=None, season=None, country=None):
    df = load_olympics()
    filtered = df.copy()

    if year is not None:
        filtered = filtered[filtered["year"] == int(year)]
    if season is not None and str(season).strip().lower() != "all":
        filtered = filtered[filtered["season"].str.lower() == str(season).strip().lower()]
    if country is not None:
        filtered = filtered[filtered["country"].str.lower() == str(country).strip().lower()]

    if filtered.empty:
        return go.Figure()

    fig = px.histogram(filtered, x="age", nbins=20, title="Age Distribution")
    return fig


def scatter_plot(year=None, season=None, country=None):
    df = load_olympics()
    filtered = df.copy()

    if year is not None:
        filtered = filtered[filtered["year"] == int(year)]
    if season is not None and str(season).strip().lower() != "all":
        filtered = filtered[filtered["season"].str.lower() == str(season).strip().lower()]
    if country is not None:
        filtered = filtered[filtered["country"].str.lower() == str(country).strip().lower()]

    if filtered.empty:
        return go.Figure()

    fig = px.scatter(
        filtered,
        x="height",
        y="weight",
        color="sex",
        hover_name="name",
        title="Height vs Weight",
    )
    return fig


def treemap(year=None, season=None, country=None):
    df = load_olympics()
    filtered = df.copy()

    if year is not None:
        filtered = filtered[filtered["year"] == int(year)]
    if season is not None and str(season).strip().lower() != "all":
        filtered = filtered[filtered["season"].str.lower() == str(season).strip().lower()]
    if country is not None:
        filtered = filtered[filtered["country"].str.lower() == str(country).strip().lower()]

    medal_df = filtered[filtered["medal"] != "No Medal"]
    if medal_df.empty:
        return go.Figure()

    counts = medal_df.groupby(["country", "sport"]).size().reset_index(name="medals")
    fig = px.treemap(counts, path=["country", "sport"], values="medals", title="Medals by Country and Sport")
    return fig


__all__ = [
    "bar_chart",
    "line_chart",
    "pie_chart",
    "heatmap",
    "histogram",
    "scatter_plot",
    "treemap",
]
