"""About page layout for the Data & Democracy 2025 application."""

from dash import html

layout = html.Div(
    style={"padding": "40px", "maxWidth": "800px", "margin": "auto"},
    children=[
        html.H2("About the Project", style={"fontWeight": "bold"}),
        html.P(
            "Currently, there is no comprehensive election results repository in a machine readable format. Much of this data is contained in scanned PDF files."
        ),
        html.P(
            "The purpose of this project is to test modern tools, specifically Large Language Models (LLMs), on this data to create a comprehensive results repository. "
            "Specifically we wish to test Claude and OpenAI's APIs on these PDFs to build a dataset in CSV form that can be contributed to the "
            "OpenElections repositories."
            "The goal of OpenElections is to create the first free, comprehensive, standardized, linked set of election data for the United States, including federal and statewide offices. We believe that we can contribute federal level data to their project."
        ),
        html.H3("Contributors", style={"marginTop": "30px"}),
        html.P("This project was started in Winter 2025 by the following team:"),
        html.Ul(
            [
                html.Li("Mentor: Francesco Colapinto (DSI Post-doc)"),
                html.Li("TA: Harper Schwab (Data Science and Human Rights, 2025)"),
                html.Li("Students:"),
                html.Ul(
                    [
                        html.Li(
                            "Sally North (Economics, Statistics, and Data Science, 2025)"
                        ),
                        html.Li("Jacob Chui (Economics and Data Science, 2025)"),
                        html.Li("Lisa Raj Singh (Sociology and Data Science, 2025)"),
                    ]
                ),
            ]
        ),
        html.P("In Spring 2025, the team was joined by:"),
        html.Ul(
            [
                html.Li("Mentor: Julia Mendelsohn (DSI Post-doc)"),
                html.Li(
                    "Student: Klaudia Barbarossa (Economics and Data Science, 2026)"
                ),
            ]
        ),
        html.P(
            "The University of Chicago Data Science Clinic is run by Tim Hannifan and Nick Ross. "
            "The students listed above worked on this project to fulfill the two-quarter clinic requirement of the Data Science Major."
        ),
        html.H3("Code", style={"marginTop": "30px"}),
        html.P("View our code on "),
        html.A(
            "GitHub",
            href="https://github.com/dsi-clinic/2025-winter-data-and-democracy",
            target="_blank",
            style={"color": "#0d6efd", "textDecoration": "underline"},
        ),
    ],
)
