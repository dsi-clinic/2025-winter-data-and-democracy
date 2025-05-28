"""Data page layout displaying available datasets and processing information."""

from dash import html

layout = html.Div(
    style={"padding": "40px", "maxWidth": "900px", "margin": "auto"},
    children=[
        html.H2("Available Datasets", style={"fontWeight": "bold"}),
        html.P(
            "Below you'll find our processed election data in machine-readable formats:"
        ),
        html.H3("Data Format", style={"marginTop": "30px"}),
        html.P(
            "Our data follows the specifications of the Open Elections project. "
            "We have data at the federal level containing the following variables: "
            "year, state, candidate name, candidate party, district (for house races), and votes. "
            "These are available as .csv files for the user to download."
        ),
        html.H3("Data Processing Pipeline", style={"marginTop": "30px"}),
        html.Ul(
            [
                html.Li("3000+ PDFs scraped from the US House site."),
                html.Li("PDFs converted to PNGs for Claude API."),
                html.Li("LLMs (Claude) extracted raw CSVs."),
                html.Li("Prompt refinement ensured full variable extraction."),
                html.Li(
                    "Prompting parameters: system, temperature, max tokens, model."
                ),
                html.Li(
                    "Accuracy checks: Levenshtein for strings, digit-level for numbers."
                ),
                html.Li(
                    "Final accuracy: 100% (most fields), 94% (candidate), 98% (votes)."
                ),
            ]
        ),
        html.P(
            "Final .csv files were submitted to the Open Elections GitHub and are downloadable here."
        ),
        html.H3("Raw Data Sources", style={"marginTop": "30px"}),
        html.A(
            "US House Election Statistics",
            href="https://history.house.gov/Institution/Election-Statistics/Election-Statistics/",
            target="_blank",
            style={"color": "#0d6efd", "textDecoration": "underline"},
        ),
    ],
)
