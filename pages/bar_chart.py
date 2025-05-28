"""Module for creating bar charts of 1932 election data by state and party."""

from pathlib import Path

import pandas as pd
import plotly.express as px

# Dynamically resolve path
csv_path = Path(__file__).resolve().parents[2] / "output" / "csv" / "1932.csv"

# Define correct columns based on your raw data
column_names = [
    "state",
    "year",
    "office",
    "district",
    "candidate_name",
    "party",
    "votes",
]

# Read with no header, assigning column names manually
election_data = pd.read_csv(
    csv_path, names=column_names, header=None, on_bad_lines="skip"
)
print(f"✅ Loaded {len(election_data)} rows from 1932.csv")
print("🧾 Columns:", election_data.columns.tolist())

# Normalize
election_data["votes"] = pd.to_numeric(election_data["votes"], errors="coerce")
election_data = election_data[election_data["votes"].notna()]

# Optional: Filter to major races
election_data = election_data[election_data["office"].isin(["Presidential", "House"])]

# Aggregate total votes by state and party
grouped = election_data.groupby(["state", "party"], as_index=False)["votes"].sum()

# Chart
fig = px.bar(
    grouped,
    x="state",
    y="votes",
    color="party",
    title="1932 Election: Party Vote Share by State",
    labels={"votes": "Total Votes"},
)
fig.update_layout(barmode="stack", xaxis_title="State", yaxis_title="Total Votes")
fig.show()
