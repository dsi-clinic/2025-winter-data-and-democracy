"""Bar chart visualization page for election data analysis."""

import pandas as pd
import plotly.express as px
from pathlib import Path
from dash import dcc, html
import dash_bootstrap_components as dbc

# Load and prepare data
def load_election_data():
    """Load and process election data from CSV files."""
    # Dynamically resolve path to the csv directory
    csv_dir = Path(__file__).resolve().parents[2] / "output" / "csv"
    
    # Define correct columns based on your raw data
    column_names = [
        "state", "year", "office", "district", "candidate_name", "party", "votes"
    ]
    
    # Find all CSV files in the directory
    csv_files = list(csv_dir.glob("*.csv"))
    
    if not csv_files:
        # Return empty dataframe if no files found
        return pd.DataFrame(columns=column_names)
    
    # Read and combine all CSV files
    all_data = []
    for csv_file in csv_files:
        temp_data = pd.read_csv(csv_file, names=column_names, header=None, on_bad_lines="skip")
        all_data.append(temp_data)
    
    # Combine all dataframes
    election_data = pd.concat(all_data, ignore_index=True)
    
    # Normalize
    election_data["votes"] = pd.to_numeric(election_data["votes"], errors="coerce")
    election_data = election_data[election_data["votes"].notna()]
    
    # Filter to major races
    election_data = election_data[election_data["office"].isin(["Presidential", "House"])]
    
    return election_data

# Load data once when module is imported
try:
    df = load_election_data()
    available_years = sorted(df["year"].unique()) if not df.empty else []
    available_offices = sorted(df["office"].unique()) if not df.empty else []
    available_states = sorted(df["state"].unique()) if not df.empty else []
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()
    available_years = []
    available_offices = []
    available_states = []

# Create the layout
layout = html.Div([
    dbc.Container([
        html.H1("Election Results Bar Chart", className="text-center mb-4"),
        
        html.P(
            "Explore election results by year, office type, and state. "
            "This visualization shows vote totals by party across different elections.",
            className="text-center mb-4"
        ),
        
        # Controls
        dbc.Row([
            dbc.Col([
                html.Label("Select Year:", className="form-label"),
                dcc.Dropdown(
                    id="bar-year-dropdown",
                    options=[{"label": str(year), "value": year} for year in available_years],
                    value=available_years[0] if available_years else None,
                    placeholder="Select a year"
                )
            ], md=4),
            
            dbc.Col([
                html.Label("Select Office:", className="form-label"),
                dcc.Dropdown(
                    id="bar-office-dropdown",
                    options=[{"label": office, "value": office} for office in available_offices],
                    value=available_offices[0] if available_offices else None,
                    placeholder="Select office type"
                )
            ], md=4),
            
            dbc.Col([
                html.Label("Filter by State (optional):", className="form-label"),
                dcc.Dropdown(
                    id="bar-state-dropdown",
                    options=[{"label": "All States", "value": "all"}] + 
                            [{"label": state, "value": state} for state in available_states],
                    value="all",
                    placeholder="Select a state"
                )
            ], md=4),
        ], className="mb-4"),
        
        # Chart
        dcc.Graph(id="bar-chart-graph"),
        
        # Data info
        html.Div(id="bar-chart-info", className="mt-3 text-muted text-center")
        
    ], fluid=True)
])

def update_bar_chart(year, office, state_filter):
    """Update bar chart based on selected filters."""
    if df.empty or not year or not office:
        return {
            "data": [],
            "layout": {
                "title": "No data available",
                "xaxis": {"title": "State"},
                "yaxis": {"title": "Votes"}
            }
        }
    
    # Filter data
    filtered_data = df[
        (df["year"] == year) & 
        (df["office"] == office)
    ].copy()
    
    if state_filter and state_filter != "all":
        filtered_data = filtered_data[filtered_data["state"] == state_filter]
    
    if filtered_data.empty:
        return {
            "data": [],
            "layout": {
                "title": f"No data available for {office} in {year}",
                "xaxis": {"title": "State"},
                "yaxis": {"title": "Votes"}
            }
        }
    
    # Aggregate votes by state and party
    grouped = filtered_data.groupby(["state", "party"], as_index=False)["votes"].sum()
    
    # Create bar chart
    fig = px.bar(
        grouped,
        x="state",
        y="votes",
        color="party",
        title=f"{year} {office} Election: Vote Share by State" + 
              (f" - {state_filter}" if state_filter != "all" else ""),
        labels={"votes": "Total Votes", "state": "State", "party": "Party"},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        barmode="group",
        xaxis_title="State",
        yaxis_title="Total Votes",
        hovermode="x unified",
        legend_title="Party"
    )
    
    # Rotate x-axis labels if many states
    if len(grouped["state"].unique()) > 10:
        fig.update_xaxes(tickangle=45)
    
    return fig
