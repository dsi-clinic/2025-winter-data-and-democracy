"""Map visualization module for displaying US election majority party data by state."""

import os
from pathlib import Path

import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

app = dash.Dash(__name__)
server = app.server

data_dir = "output/csv"

# Load available years
available_years = sorted(
    [
        int(fname.split(".")[0])
        for fname in os.listdir(data_dir)
        if fname.endswith(".csv") and fname.split(".")[0].isdigit()
    ]
)

party_color_map = {
    "DEMOCRAT": "blue",
    "REPUBLICAN": "red",
    "SOCIALIST": "green",
    "PROGRESSIVE": "purple",
    "OTHER": "gray",
}


def process_majority_party(file_path, race_type, selected_year):
    """Process election data to determine majority party by state for visualization.

    Args:
        file_path: Path to the CSV file containing election data
        race_type: Type of race (HOUSE or SENATE)
        selected_year: Year to filter data for

    Returns:
        Plotly choropleth figure showing majority party by state
    """
    try:
        election_data = pd.read_csv(file_path, header=None, on_bad_lines="skip")
    except Exception as e:
        return px.choropleth(title=f"Failed to load data: {e}")

    # Find header
    expected_cols = 7
    for i, row in election_data.iterrows():
        if len(row.dropna()) >= expected_cols:
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
        return px.choropleth(title="No valid header found")

    election_data.columns = [str(col).upper().strip() for col in election_data.columns]
    for col in ["STATE", "RACE_TYPE", "CANDIDATE_PARTY"]:
        if col in election_data.columns:
            election_data[col] = election_data[col].astype(str).str.upper().str.strip()

    election_data["YEAR"] = pd.to_numeric(election_data["YEAR"], errors="coerce")
    election_data = election_data[election_data["YEAR"] == selected_year]

    race_labels = [race_type.upper()]
    if race_type.upper() == "HOUSE":
        race_labels += ["REPRESENTATIVE"]
    elif race_type.upper() == "SENATE":
        race_labels += ["SENATOR"]

    election_data = election_data[election_data["RACE_TYPE"].isin(race_labels)]
    election_data["VOTES"] = pd.to_numeric(election_data["VOTES"], errors="coerce")
    election_data = election_data.dropna(subset=["STATE", "CANDIDATE_PARTY", "VOTES"])

    if election_data.empty:
        return px.choropleth(title=f"No {race_type} race data available")

    majority_party = (
        election_data.groupby(["STATE", "CANDIDATE_PARTY"])["VOTES"]
        .sum()
        .reset_index()
        .sort_values(["STATE", "VOTES"], ascending=[True, False])
        .drop_duplicates("STATE")
    )

    state_abbrev = pd.read_csv(
        "https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv"
    )
    state_abbrev.columns = state_abbrev.columns.str.upper()
    state_abbrev["STATE"] = state_abbrev["STATE"].str.upper().str.strip()

    majority_party = majority_party.merge(state_abbrev, on="STATE", how="left")
    majority_party = majority_party.dropna(subset=["ABBREVIATION"])

    majority_party["COLOR"] = majority_party["CANDIDATE_PARTY"].map(
        lambda x: party_color_map.get(x.upper(), "gray")
    )

    fig = px.choropleth(
        majority_party,
        locations="ABBREVIATION",
        locationmode="USA-states",
        color="CANDIDATE_PARTY",
        color_discrete_map=party_color_map,
        hover_name="STATE",
        hover_data={"CANDIDATE_PARTY": True, "VOTES": True, "ABBREVIATION": False},
        scope="usa",
        title=f"Majority Party in US {race_type.title()} Elections by State ({selected_year})",
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
            ],
        ),
        dcc.Graph(id="choropleth-map"),
    ]
)


@app.callback(
    Output("choropleth-map", "figure"),
    Input("year-dropdown", "value"),
    Input("race-tabs", "value"),
)
def update_map(year, race):
    """Update the choropleth map based on selected year and race type.

    Args:
        year: Selected year for election data
        race: Selected race type (HOUSE or SENATE)

    Returns:
        Updated plotly figure for the map
    """
    file_path = Path(data_dir) / f"{year}.csv"
    return process_majority_party(file_path, race, selected_year=year)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
