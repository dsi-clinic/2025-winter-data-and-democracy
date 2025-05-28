"""Main application module for the Data & Democracy 2025 web application."""
import os
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from pages.about import layout as about_layout
from pages.data import layout as data_layout
from pages.data_viewer import layout as data_viewer_layout
from pages.home import layout as home_layout
# Import map visualization
from pages import map_viz

def create_app():
    """Create and configure the Dash application with navigation and routing."""
    app = Dash(
        __name__,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )
    
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/", style={"color": "black"})),
            dbc.NavItem(dbc.NavLink("About", href="/about", style={"color": "black"})),
            dbc.NavItem(dbc.NavLink("Data", href="/data", style={"color": "black"})),
            dbc.NavItem(
                dbc.NavLink(
                    "Data Viewer", href="/data-viewer", style={"color": "black"}
                )
            ),
            dbc.NavItem(
                dbc.NavLink(
                    "Map Visualization", href="/map", style={"color": "black"}
                )
            ),
        ],
        brand="Data & Democracy 2025",
        brand_href="/",
        color="light",
        dark=False,
        style={
            "background": "rgba(255, 255, 255, 0.95)",
            "boxShadow": "0px 4px 6px rgba(0,0,0,0.1)",
        },
    )
    
    app.layout = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])
    
    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def display_page(pathname):
        if pathname == "/" or pathname == "/index":
            return html.Div([navbar, home_layout])
        elif pathname == "/about":
            return html.Div([navbar, about_layout])
        elif pathname == "/data":
            return html.Div([navbar, data_layout])
        elif pathname == "/data-viewer":
            return html.Div([navbar, data_viewer_layout])
        elif pathname == "/map":
            return html.Div([navbar, map_viz.layout])
        else:
            return html.Div(
                [navbar, html.H2("404 - Page Not Found", className="text-center mt-5")]
            )
    
    # Register the map visualization callback
    @app.callback(
        Output("choropleth-map", "figure"),
        Input("year-dropdown", "value"),
        Input("race-tabs", "value"),
        Input("margin-toggle", "value"),
    )
    def update_map_callback(year, race, margin_toggle):
        return map_viz.update_map(year, race, margin_toggle)
    
    return app

def main():
    """Run the application with specified host and port configuration."""
    app = create_app()
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
