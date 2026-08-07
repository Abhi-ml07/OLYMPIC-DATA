from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[1]
athlete_events_path = project_root / "data" / "athlete_events.csv"

athletes = pd.read_csv(athlete_events_path, encoding="latin1")
olympics = athletes.copy()
olympics["country"] = olympics["NOC"]
olympics = olympics.drop(columns=["NOC"])

olympics = olympics.drop_duplicates().reset_index(drop=True)

olympics["Medal"] = olympics["Medal"].fillna("No Medal")


for column in ["Age", "Height", "Weight"]:
    if column in olympics.columns:
        olympics[column] = olympics[column].fillna(olympics[column].mean())

olympics["Age"] = olympics["Age"].astype("int16")

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
).reset_index(drop=True)

print(olympics.head())
print(f"Cleaned dataset shape: {olympics.shape}")