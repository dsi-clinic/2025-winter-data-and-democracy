from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div(
    style={
        "height": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center",
        "textAlign": "center",
        "backgroundColor": "#f8f9fa",
        "padding": "40px",
    },
    children=[
        html.H1(
            "Welcome to the Data & Democracy Project",
            style={"fontSize": "42px", "fontWeight": "bold", "marginBottom": "20px"},
        ),
        html.P(
            "This project aims to make historical U.S. election results machine-readable and publicly accessible.",
            style={"fontSize": "20px", "maxWidth": "700px"},
        ),
        html.Div(
            [
                dcc.Link(
                    dbc.Button("Explore About Page", color="primary", className="m-2"),
                    href="/about"
                ),
                dcc.Link(
                    dbc.Button("View Processed Data", color="secondary", className="m-2"),
                    href="/data"
                ),
                dcc.Link(
                    dbc.Button("Open Data Viewer", color="info", className="m-2"),
                    href="/data-viewer"
                ),
            ],
            style={"marginTop": "30px"},
        )
    ]
)
