from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Import page layouts
from pages.home import layout as home_layout
from pages.about import layout as about_layout
from pages.data import layout as data_layout
from pages.data_viewer import layout as data_viewer_layout

def create_app():
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
            dbc.NavItem(dbc.NavLink("Data Viewer", href="/data-viewer", style={"color": "black"})),
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

    app.layout = html.Div([
        dcc.Location(id="url"),
        html.Div(id="page-content")
    ])

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
        else:
            return html.Div([navbar, html.H2("404 - Page Not Found", className="text-center mt-5")])

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()
