"""Map visualization module for displaying US election majority party data by state."""

import os
from pathlib import Path
from typing import Literal

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

app = Dash(__name__)
server = app.server

DATA_DIR = "output/csv"

# Expected number of columns in election data
EXPECTED_COLUMNS = 7

# Available election years
available_years = sorted(
    int(f.split(".")[0])
    for f in os.listdir(DATA_DIR)
    if f.endswith(".csv") and f.split(".")[0].isdigit()
)

# Party color map
party_color_map = {
    "DEMOCRAT": "blue",
    "REPUBLICAN": "red",
    "SOCIALIST": "green",
    "PROGRESSIVE": "purple",
    "OTHER": "gray",
}


def load_cleaned_data(file_path: str) -> pd.DataFrame:
    """Load CSV file while skipping malformed lines and headers."""
    election_data = pd.read_csv(file_path, header=None, on_bad_lines="skip")

    for i, row in election_data.iterrows():
        if len(row.dropna()) >= EXPECTED_COLUMNS:
            election_data.columns = [
                "STATE",
                "YEAR",
                "RACE_TYPE",
                "CONGRESSIONAL_DISTRICT",
                "CANDIDATE_NAME",
                "CANDIDATE_PARTY",
                "VOTES",
            ]
            election_data = election_data.iloc[i + 1 :].copy()
            break
    else:
        return pd.DataFrame()  # no valid header found

    election_data.columns = election_data.columns.str.upper().str.strip()

    for col in ["STATE", "RACE_TYPE", "CANDIDATE_PARTY"]:
        election_data[col] = election_data[col].astype(str).str.upper().str.strip()

    election_data["VOTES"] = pd.to_numeric(election_data["VOTES"], errors="coerce")
    election_data["YEAR"] = pd.to_numeric(election_data["YEAR"], errors="coerce")
    election_data = election_data.dropna(
        subset=["STATE", "CANDIDATE_PARTY", "VOTES", "YEAR"]
    )

    return election_data


def process_majority_party(
    file_path: str,
    race_type: Literal["HOUSE", "SENATE", "PRESIDENTIAL"],
    show_margin: bool = False,
) -> px.choropleth:
    """Process election data to create choropleth map showing majority party by state.

    Args:
        file_path: Path to the CSV file containing election data
        race_type: Type of race (HOUSE, SENATE, or PRESIDENTIAL)
        show_margin: Whether to show margin of victory instead of party colors

    Returns:
        Plotly choropleth figure showing majority party or margin by state
    """
    election_data = load_cleaned_data(file_path)
    if election_data.empty:
        return px.choropleth(title="No usable data found")

    year = int(Path(file_path).name.split(".")[0])
    election_data = election_data[election_data["YEAR"] == year]

    race_aliases = {
        "HOUSE": ["HOUSE", "REPRESENTATIVE"],
        "SENATE": ["SENATE", "SENATOR"],
        "PRESIDENTIAL": ["PRESIDENTIAL", "PRESIDENT"],
    }
    election_data = election_data[
        election_data["RACE_TYPE"].isin(race_aliases[race_type])
    ]

    if election_data.empty:
        return px.choropleth(title=f"No {race_type.title()} data for {year}")

    # Compute majority + margin
    grouped = (
        election_data.groupby(["STATE", "CANDIDATE_PARTY"])["VOTES"]
        .sum()
        .reset_index()
        .sort_values(["STATE", "VOTES"], ascending=[True, False])
    )
    top_two = grouped.groupby("STATE").head(2)

    def margin_calc(group: pd.DataFrame) -> pd.Series:
        if len(group) == 1:
            return pd.Series({"WINNER": group.iloc[0]["CANDIDATE_PARTY"], "MARGIN": 0})
        margin = group.iloc[0]["VOTES"] - group.iloc[1]["VOTES"]
        return pd.Series({"WINNER": group.iloc[0]["CANDIDATE_PARTY"], "MARGIN": margin})

    result = top_two.groupby("STATE").apply(margin_calc).reset_index()

    # Map to abbreviations
    abbrev = pd.read_csv(
        "https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv"
    )
    abbrev.columns = abbrev.columns.str.upper()
    abbrev["STATE"] = abbrev["STATE"].str.upper().str.strip()

    result = result.merge(abbrev, on="STATE", how="left")
    result = result.dropna(subset=["ABBREVIATION"])

    if show_margin:
        fig = px.choropleth(
            result,
            locations="ABBREVIATION",
            locationmode="USA-states",
            color="MARGIN",
            hover_name="STATE",
            hover_data={"WINNER": True, "MARGIN": True},
            color_continuous_scale="RdBu",
            scope="usa",
            title=f"Majority Party in US {race_type.title()} Elections by State ({year})",
        )
    else:
        color_map = {
            key: party_color_map.get(key.upper(), "gray")
            for key in result["WINNER"].unique()
        }
        fig = px.choropleth(
            result,
            locations="ABBREVIATION",
            locationmode="USA-states",
            color="WINNER",
            color_discrete_map=color_map,
            hover_name="STATE",
            hover_data={"WINNER": True, "MARGIN": True},
            scope="usa",
            title=f"Majority Party in US {race_type.title()} Elections by State ({year})",
        )
    return fig


app.layout = html.Div(
    [
        html.H1("US Elections: Majority Party by State"),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": str(y), "value": y} for y in available_years],
            value=available_years[0],
            style={"width": "300px"},
        ),
        dcc.Tabs(
            id="race-tabs",
            value="HOUSE",
            children=[
                dcc.Tab(label="House", value="HOUSE"),
                dcc.Tab(label="Senate", value="SENATE"),
                dcc.Tab(label="Presidential", value="PRESIDENTIAL"),
            ],
        ),
        dcc.Checklist(
            id="margin-toggle",
            options=[{"label": "Show Margin of Victory", "value": "SHOW_MARGIN"}],
            value=[],
            style={"margin": "1em 0"},
        ),
        dcc.Graph(id="choropleth-map"),
    ]
)


@app.callback(
    Output("choropleth-map", "figure"),
    Input("year-dropdown", "value"),
    Input("race-tabs", "value"),
    Input("margin-toggle", "value"),
)
def update_map(year: int, race: str, margin_toggle: list[str]) -> px.choropleth:
    """Update the choropleth map based on selected year, race type, and margin toggle.

    Args:
        year: Selected year for election data
        race: Selected race type (HOUSE, SENATE, or PRESIDENTIAL)
        margin_toggle: List containing 'SHOW_MARGIN' if margin view is enabled

    Returns:
        Updated plotly choropleth figure for the map
    """
    file_path = Path(DATA_DIR) / f"{year}.csv"
    return process_majority_party(
        str(file_path), race, show_margin="SHOW_MARGIN" in margin_toggle
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
