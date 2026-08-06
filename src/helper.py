from functools import lru_cache
from pathlib import Path

import pandas as pd


@lru_cache(maxsize=1)
def load_olympics() -> pd.DataFrame:
    project_root = Path(__file__).resolve().parents[1]
    athlete_events_path = project_root / "data" / "athlete_events.csv"

    athletes = pd.read_csv(athlete_events_path, encoding="latin1")
    olympics = athletes.copy()
    olympics["country"] = olympics["NOC"]
    olympics = olympics.drop(columns=["NOC"])

    olympics = olympics.drop_duplicates().reset_index(drop=True)
    olympics["Medal"] = olympics["Medal"].fillna("No Medal")

    for column in ["Age", "Height", "Weight"]:
        olympics[column] = olympics[column].fillna(olympics[column].median())

    olympics = olympics.rename(
        columns={
            "ID": "id",
            "Name": "name",
            "Sex": "sex",
            "Age": "age",
            "Height": "height",
            "Weight": "weight",
            "Team": "team",
            "Country": "country",
            "Games": "games",
            "Year": "year",
            "Season": "season",
            "City": "city",
            "Sport": "sport",
            "Event": "event",
            "Medal": "medal",
        }
    )
    return olympics


def _filter_data(df: pd.DataFrame, year=None, season=None, country=None, athlete=None):
    filtered = df.copy()

    if year is not None:
        filtered = filtered[filtered["year"] == int(year)]
    if season is not None and str(season).strip().lower() != "all":
        filtered = filtered[filtered["season"].str.lower() == str(season).strip().lower()]
    if country is not None:
        filtered = filtered[filtered["country"].str.lower() == str(country).strip().lower()]
    if athlete is not None:
        filtered = filtered[filtered["name"].str.lower().str.contains(str(athlete).strip().lower(), na=False)]

    return filtered


def medal_tally(year=None, season=None, country=None) -> pd.DataFrame:
    df = _filter_data(load_olympics(), year=year, season=season, country=country)
    medal_df = df[df["medal"] != "No Medal"]

    if medal_df.empty:
        return pd.DataFrame(columns=["Gold", "Silver", "Bronze", "Total"])

    tally = (
        medal_df.groupby("country")["medal"]
        .value_counts()
        .unstack(fill_value=0)
        .reindex(columns=["Gold", "Silver", "Bronze"], fill_value=0)
    )
    tally["Total"] = tally.sum(axis=1)
    return tally.sort_values("Total", ascending=False)


def country_analysis(year=None, season=None, country=None) -> pd.DataFrame:
    df = _filter_data(load_olympics(), year=year, season=season, country=country)

    summary = (
        df.groupby("country")
        .agg(
            athletes=("name", "nunique"),
            medals=("medal", lambda s: (s != "No Medal").sum()),
            golds=("medal", lambda s: (s == "Gold").sum()),
            silvers=("medal", lambda s: (s == "Silver").sum()),
            bronzes=("medal", lambda s: (s == "Bronze").sum()),
            sports=("sport", "nunique"),
            events=("event", "nunique"),
            games=("games", "nunique"),
        )
        .reset_index()
    )
    return summary.sort_values(["medals", "golds"], ascending=False).reset_index(drop=True)


def athlete_analysis(athlete=None, year=None, season=None) -> pd.DataFrame:
    df = _filter_data(load_olympics(), year=year, season=season, athlete=athlete)

    summary = (
        df.groupby(["name", "country"])
        .agg(
            medals=("medal", lambda s: (s != "No Medal").sum()),
            golds=("medal", lambda s: (s == "Gold").sum()),
            silvers=("medal", lambda s: (s == "Silver").sum()),
            bronzes=("medal", lambda s: (s == "Bronze").sum()),
            sports=("sport", "nunique"),
            events=("event", "nunique"),
            appearances=("games", "nunique"),
        )
        .reset_index()
    )
    return summary.sort_values(["medals", "golds"], ascending=False).reset_index(drop=True)


def top_athletes(n=10, year=None, season=None) -> pd.DataFrame:
    return athlete_analysis(year=year, season=season).head(n)


def top_countries(n=10, year=None, season=None) -> pd.DataFrame:
    return country_analysis(year=year, season=season).head(n)


def gender_analysis(year=None, season=None) -> pd.DataFrame:
    df = _filter_data(load_olympics(), year=year, season=season)

    summary = (
        df.groupby("sex")
        .agg(
            athletes=("name", "nunique"),
            medals=("medal", lambda s: (s != "No Medal").sum()),
            golds=("medal", lambda s: (s == "Gold").sum()),
            silvers=("medal", lambda s: (s == "Silver").sum()),
            bronzes=("medal", lambda s: (s == "Bronze").sum()),
        )
        .reset_index()
    )
    return summary.sort_values(["medals", "golds"], ascending=False).reset_index(drop=True)


def age_analysis(year=None, season=None) -> pd.DataFrame:
    df = _filter_data(load_olympics(), year=year, season=season)

    summary = (
        df.groupby("sport")
        .agg(
            athletes=("name", "nunique"),
            avg_age=("age", "mean"),
            medal_winners=("medal", lambda s: (s != "No Medal").sum()),
            golds=("medal", lambda s: (s == "Gold").sum()),
        )
        .reset_index()
    )
    return summary.sort_values(["medal_winners", "avg_age"], ascending=[False, True]).reset_index(drop=True)


def build_athlete_record_summary(df: pd.DataFrame) -> pd.DataFrame:
    agg_spec = {
        "medals": ("medal", lambda s: (s != "No Medal").sum()),
        "golds": ("medal", lambda s: (s == "Gold").sum()),
        "silvers": ("medal", lambda s: (s == "Silver").sum()),
        "bronzes": ("medal", lambda s: (s == "Bronze").sum()),
        "appearances": ("games", "nunique"),
        "sports": ("sport", "nunique"),
        "years": ("year", "nunique"),
        "oldest_age": ("age", "max"),
        "youngest_age": ("age", "min"),
    }

    if "height" in df.columns:
        agg_spec["tallest_height"] = ("height", "max")
        agg_spec["shortest_height"] = ("height", "min")

    if "weight" in df.columns:
        agg_spec["heaviest_weight"] = ("weight", "max")
        agg_spec["lightest_weight"] = ("weight", "min")

    summary = df.groupby(["name", "country"]).agg(**agg_spec).reset_index()
    return summary.sort_values(["medals", "golds"], ascending=False).reset_index(drop=True)


def records() -> pd.DataFrame:
    return build_athlete_record_summary(load_olympics()).head(20)


def timeline(year=None, season=None, country=None) -> pd.DataFrame:
    df = _filter_data(load_olympics(), year=year, season=season, country=country)
    medal_df = df[df["medal"] != "No Medal"]

    if medal_df.empty:
        return pd.DataFrame(columns=["year", "country", "medals"])

    timeline_df = (
        medal_df.groupby(["year", "country"])
        .size()
        .reset_index(name="medals")
    )
    return timeline_df.sort_values(["year", "medals"], ascending=[True, False]).reset_index(drop=True)


__all__ = [
    "load_olympics",
    "medal_tally",
    "country_analysis",
    "athlete_analysis",
    "top_athletes",
    "top_countries",
    "gender_analysis",
    "age_analysis",
    "records",
    "build_athlete_record_summary",
    "timeline",
]
