"""Module for creating bar charts of 1932 election data by state and party."""

import pandas as pd
import plotly.express as px
from pathlib import Path


def load_election_data():
    """Load and process 1932 election data from CSV file."""
    # Try multiple possible paths for the CSV file
    possible_paths = [
        Path(__file__).resolve().parent.parent / "data" / "1932.csv",
        Path("data/1932.csv"),
        Path(__file__).resolve().parents[2] / "output" / "csv" / "1932.csv",
        Path(__file__).resolve().parent.parent / "output" / "csv" / "1932.csv",
        Path("output/csv/1932.csv"),
        Path("../output/csv/1932.csv"),
        Path("../../output/csv/1932.csv"),
    ]
    
    csv_path = None
    for path in possible_paths:
        if path.exists():
            csv_path = path
            break
    
    if csv_path is None:
        raise FileNotFoundError(
            f"Could not find 1932.csv in any of these locations: {[str(p) for p in possible_paths]}"
        )
    
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
    print(f"✅ Loaded {len(election_data)} rows from {csv_path}")
    print("🧾 Columns:", election_data.columns.tolist())
    
    # Normalize
    election_data["votes"] = pd.to_numeric(election_data["votes"], errors="coerce")
    election_data = election_data[election_data["votes"].notna()]
    
    # Optional: Filter to major races
    election_data = election_data[election_data["office"].isin(["Presidential", "House"])]
    
    return election_data


def create_bar_chart():
    """Create and display bar chart of election data."""
    try:
        election_data = load_election_data()
        
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
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please ensure the 1932.csv file is in the correct location.")


def create_dash_layout():
    """Create Dash layout component for the bar chart page."""
    import dash
    from dash import dcc, html
    import plotly.graph_objects as go
    
    try:
        election_data = load_election_data()
        
        # Aggregate total votes by state and party
        grouped = election_data.groupby(["state", "party"], as_index=False)["votes"].sum()
        
        # Create the figure
        fig = px.bar(
            grouped,
            x="state",
            y="votes",
            color="party",
            title="1932 Election: Party Vote Share by State",
            labels={"votes": "Total Votes"},
        )
        fig.update_layout(barmode="stack", xaxis_title="State", yaxis_title="Total Votes")
        
        # Return Dash layout
        return html.Div([
            html.H1("1932 Election Results", className="text-center mb-4"),
            dcc.Graph(
                id="election-bar-chart",
                figure=fig,
                style={"height": "600px"}
            ),
            html.P(
                f"Data loaded: {len(election_data)} records processed",
                className="text-muted text-center"
            )
        ])
        
    except FileNotFoundError as e:
        return html.Div([
            html.H1("Data Loading Error", className="text-center mb-4"),
            html.Div([
                html.P(f"❌ Error: {e}", className="alert alert-danger"),
                html.P("Please ensure the 1932.csv file is in the correct location.", 
                       className="text-muted")
            ])
        ])


# Create the layout that main.py expects
layout = create_dash_layout()

# Only run if this file is executed directly
if __name__ == "__main__":
    create_bar_chart()
