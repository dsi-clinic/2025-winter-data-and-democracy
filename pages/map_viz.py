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

# Maximum number of rows to check for headers
MAX_HEADER_CHECK_ROWS = 10

# Available election years
available_years = sorted(
    int(f.split(".")[0])
    for f in os.listdir(DATA_DIR)
    if f.endswith(".csv") and f.split(".")[0].isdigit()
)

# Party color map - expanded to handle more variations
party_color_map = {
    "DEMOCRAT": "blue",
    "DEMOCRATIC": "blue",
    "DEM": "blue",
    "REPUBLICAN": "red",
    "REP": "red",
    "SOCIALIST": "green",
    "PROGRESSIVE": "purple",
    "LIBERTARIAN": "yellow",
    "GREEN": "darkgreen",
    "INDEPENDENT": "gray",
    "IND": "gray",
    "OTHER": "lightgray",
}


def load_cleaned_data(file_path: str) -> pd.DataFrame:
    """Load CSV file while skipping malformed lines and headers."""
    try:
        election_data = pd.read_csv(
            file_path, header=None, on_bad_lines="skip", encoding="utf-8"
        )
    except UnicodeDecodeError:
        try:
            election_data = pd.read_csv(
                file_path, header=None, on_bad_lines="skip", encoding="latin-1"
            )
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return pd.DataFrame()

    if election_data.empty:
        return pd.DataFrame()

    # Find header row more robustly
    header_found = False
    for i, row in election_data.iterrows():
        # Check if this looks like a header row
        non_null_count = len(row.dropna())
        if non_null_count >= EXPECTED_COLUMNS:
            # Check if this row contains expected header-like values
            row_str = " ".join(
                str(val).upper() for val in row.dropna() if pd.notna(val)
            )
            if any(
                keyword in row_str
                for keyword in ["STATE", "YEAR", "RACE", "CANDIDATE", "PARTY", "VOTES"]
            ):
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
                header_found = True
                break
            # If no header keywords found but has enough columns, assume it's data
            elif (
                non_null_count == EXPECTED_COLUMNS and i < MAX_HEADER_CHECK_ROWS
            ):  # Only check first few rows
                election_data.columns = [
                    "STATE",
                    "YEAR",
                    "RACE_TYPE",
                    "CONGRESSIONAL_DISTRICT",
                    "CANDIDATE_NAME",
                    "CANDIDATE_PARTY",
                    "VOTES",
                ]
                election_data = election_data.iloc[i:].copy()
                header_found = True
                break

    if not header_found:
        print(f"No valid header found in {file_path}")
        return pd.DataFrame()

    # Clean column names
    election_data.columns = [str(col).upper().strip() for col in election_data.columns]

    # Clean string columns - handle NaN values AND case sensitivity properly
    string_columns = ["STATE", "CANDIDATE_PARTY", "CANDIDATE_NAME"]
    for col in string_columns:
        if col in election_data.columns:
            election_data[col] = (
                election_data[col]
                .astype(str)
                .replace(["nan", "NaN", "None", ""], pd.NA)
                .str.upper()
                .str.strip()
            )

    # Handle RACE_TYPE - normalize case and clean values
    if "RACE_TYPE" in election_data.columns:
        election_data["RACE_TYPE"] = (
            election_data["RACE_TYPE"]
            .astype(str)
            .replace(["nan", "NaN", "None", ""], pd.NA)
            .str.strip()
            .str.upper()  # Convert to uppercase for consistent matching
        )

    # Convert numeric columns
    election_data["VOTES"] = pd.to_numeric(election_data["VOTES"], errors="coerce")

    # FORCE the year to be the filename year - ignore whatever is in the YEAR column
    filename_year = int(Path(file_path).name.split(".")[0])
    election_data["YEAR"] = filename_year

    # Drop rows with missing critical data (don't check YEAR since we're forcing it)
    election_data = election_data.dropna(subset=["STATE", "CANDIDATE_PARTY", "VOTES"])

    # Filter out rows where essential fields are still invalid
    election_data = election_data[
        (election_data["STATE"].str.len() > 0)
        & (election_data["CANDIDATE_PARTY"].str.len() > 0)
        & (election_data["VOTES"] >= 0)
    ]

    print(f"Loaded {len(election_data)} valid records from {file_path}")
    print(f"Forced year to: {filename_year} (from filename)")
    print(f"Unique states: {sorted(election_data['STATE'].unique())}")
    print(f"Unique parties: {sorted(election_data['CANDIDATE_PARTY'].unique())}")

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

    # Debug: Print all unique race types in the data
    print(
        f"All race types in data: {sorted(election_data['RACE_TYPE'].dropna().unique())}"
    )
    print("Race type value counts:")
    print(election_data["RACE_TYPE"].value_counts())

    # Comprehensive race type matching - handle all the variations we found
    def match_race_type(race_series, target_race):
        """Match race types flexibly across different data formats"""
        # Convert to string and handle nulls
        race_clean = race_series.astype(str).str.strip().str.upper()

        if target_race == "HOUSE":
            # Match various House representations - now all uppercase
            house_patterns = [
                "HOUSE",
                "REPRESENTATIVE",
                "REPRESENTATIVES",
                "REP",
                "AT LARGE",
            ]
            return race_clean.isin(house_patterns)

        elif target_race == "SENATE":
            # Match various Senate representations - now all uppercase
            senate_patterns = ["SENATE", "SENATOR", "SEN", "SENATE_DEMOCRATS"]
            return race_clean.isin(senate_patterns)

        elif target_race == "PRESIDENTIAL":
            # Match various Presidential representations - now all uppercase
            pres_patterns = ["PRESIDENTIAL", "PRESIDENT", "PRES"]
            return race_clean.isin(pres_patterns)

        return pd.Series([False] * len(race_series))

    # Filter by race type using flexible matching
    race_filter = match_race_type(election_data["RACE_TYPE"], race_type)
    matching_records = election_data[race_filter]

    print(f"Looking for race type: {race_type}")
    print(f"Records matching race filter: {len(matching_records)}")
    print(
        f"States in matching records: {len(matching_records['STATE'].unique()) if not matching_records.empty else 0}"
    )

    election_data = matching_records

    if election_data.empty:
        return px.choropleth(title=f"No {race_type.title()} data for {year}")

    # Check if this is actually the right year's data
    actual_years = election_data["YEAR"].dropna().unique()
    if len(actual_years) > 0 and year not in actual_years:
        actual_year = actual_years[0]
        return px.choropleth(
            title=f"Warning: File {year}.csv contains {actual_year} data, not {year} data"
        )

    print(f"Processing {len(election_data)} records for {race_type} in {year}")

    # Group by state and party, sum votes
    state_party_votes = (
        election_data.groupby(["STATE", "CANDIDATE_PARTY"])["VOTES"].sum().reset_index()
    )

    # Find winner for each state
    state_winners = []
    for state in state_party_votes["STATE"].unique():
        state_data = state_party_votes[state_party_votes["STATE"] == state].copy()
        state_data = state_data.sort_values("VOTES", ascending=False)

        if len(state_data) > 0:
            winner = state_data.iloc[0]
            margin = 0
            if len(state_data) > 1:
                margin = winner["VOTES"] - state_data.iloc[1]["VOTES"]

            state_winners.append(
                {
                    "STATE": state,
                    "WINNER": winner["CANDIDATE_PARTY"],
                    "VOTES": winner["VOTES"],
                    "MARGIN": margin,
                }
            )

    if not state_winners:
        return px.choropleth(title=f"No winners determined for {race_type} in {year}")

    result = pd.DataFrame(state_winners)

    # Load state abbreviations with error handling
    try:
        abbrev = pd.read_csv(
            "https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv"
        )
        abbrev.columns = abbrev.columns.str.upper()
        abbrev["STATE"] = abbrev["STATE"].str.upper().str.strip()

        # Merge with abbreviations
        result = result.merge(abbrev, on="STATE", how="left")

        # For states without abbreviations, try some common mappings
        state_abbrev_manual = {
            "DIST. OF COLUMBIA": "DC",
            "DISTRICT OF COLUMBIA": "DC",
            "D.C.": "DC",
            "WASHINGTON D.C.": "DC",
        }

        for state, abbr in state_abbrev_manual.items():
            mask = (result["STATE"] == state) & (result["ABBREVIATION"].isna())
            result.loc[mask, "ABBREVIATION"] = abbr

    except Exception as e:
        print(f"Error loading state abbreviations: {e}")
        return px.choropleth(title="Error loading state data")

    # Remove states without abbreviations
    missing_abbrev = result[result["ABBREVIATION"].isna()]
    if not missing_abbrev.empty:
        print(
            f"Warning: No abbreviations found for states: {missing_abbrev['STATE'].tolist()}"
        )

    result = result.dropna(subset=["ABBREVIATION"])

    if result.empty:
        return px.choropleth(title="No states with valid abbreviations found")

    # Create the map
    if show_margin:
        fig = px.choropleth(
            result,
            locations="ABBREVIATION",
            locationmode="USA-states",
            color="MARGIN",
            hover_name="STATE",
            hover_data={"WINNER": True, "MARGIN": True, "VOTES": True},
            color_continuous_scale="RdBu",
            scope="usa",
            title=f"Victory Margin in US {race_type.title()} Elections by State ({year})",
        )
    else:
        # Create color mapping for parties found in data
        unique_parties = result["WINNER"].unique()
        color_map = {}
        for party in unique_parties:
            if party in party_color_map:
                color_map[party] = party_color_map[party]
            else:
                # Assign default colors for unknown parties
                color_map[party] = "lightgray"

        fig = px.choropleth(
            result,
            locations="ABBREVIATION",
            locationmode="USA-states",
            color="WINNER",
            color_discrete_map=color_map,
            hover_name="STATE",
            hover_data={"WINNER": True, "MARGIN": True, "VOTES": True},
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
            value=available_years[0] if available_years else 2020,
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
    if not file_path.exists():
        return px.choropleth(title=f"No data file found for {year}")

    return process_majority_party(
        str(file_path), race, show_margin="SHOW_MARGIN" in margin_toggle
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
