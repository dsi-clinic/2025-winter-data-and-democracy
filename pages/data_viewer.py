from pathlib import Path
from dash import dcc, html, dash_table, Input, Output, no_update, callback
import dash_bootstrap_components as dbc
import pandas as pd

CSV_DIR = Path("output/csv")

def list_csv_files():
    if not CSV_DIR.exists():
        return []
    return sorted([f.name for f in CSV_DIR.glob("*.csv")])

layout = dbc.Container(
    [
        html.H2("Historical U.S. Election Data Viewer", className="text-center my-4"),
        html.P(
            "Explore year-by-year parsed election result CSVs created as part of the "
            "2025 Winter Data and Democracy project.",
            className="text-center",
        ),
        dbc.Row([
            dbc.Col([
                html.Label("Select Election Year:"),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[{"label": f.replace('.csv', ''), "value": f} for f in list_csv_files()],
                    value="1920.csv" if "1920.csv" in list_csv_files() else None,
                    clearable=False
                ),
            ], width=6),
        ]),
        html.Hr(),
        html.H4(id="preview-title", className="mt-4"),
        dash_table.DataTable(
            id="data-table",
            page_size=15,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
        ),
        html.Div([
            html.Button("Download CSV", id="download-button", className="btn btn-primary mt-3"),
            dcc.Download(id="download-csv"),
        ], className="text-center")
    ],
    fluid=True,
)

@callback(
    Output("preview-title", "children"),
    Output("data-table", "data"),
    Output("data-table", "columns"),
    Input("year-dropdown", "value"),
)
def update_table(selected_file):
    if not selected_file:
        return "Preview:", [], []

    path = CSV_DIR / selected_file
    if not path.exists():
        return f"File not found: {selected_file}", [], []

    try:
        df = pd.read_csv(path, nrows=100)
        df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()
        return f"Preview of {selected_file}", df.to_dict("records"), [{"name": c, "id": c} for c in df.columns]
    except Exception as e:
        return f"Error loading {selected_file}: {e}", [], []

@callback(
    Output("download-csv", "data"),
    Input("download-button", "n_clicks"),
    Input("year-dropdown", "value"),
    prevent_initial_call=True,
)
def download_csv(n_clicks, selected_file):
    if selected_file:
        path = CSV_DIR / selected_file
        if path.exists():
            return dcc.send_file(str(path))
    return no_update
