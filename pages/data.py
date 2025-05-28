"""Data page layout displaying available datasets and processing information."""

from dash import html

layout = html.Div(
    style={"padding": "40px", "maxWidth": "900px", "margin": "auto"},
    children=[
        html.H2("Available Datasets", style={"fontWeight": "bold"}),
        html.P(
            "Below you'll find our processed election data in machine-readable formats. "
            "Our data follows the specifications of the Open Elections project with data at the federal level."
        ),

        html.H3("Data Format", style={"marginTop": "30px"}),
        html.P(
            "Our data contains the following variables: year, state, candidate name, candidate party, "
            "district (for house races), and votes. These are available as .csv files for download."
        ),

        html.H3("Data Coverage", style={"marginTop": "30px"}),
        html.Ul(
            [
                html.Li("Federal-level elections from 1920 to 1996"),
                html.Li("House, Senate, and Presidential election results"),
                html.Li("Over 3,000 pages of archival election data from 51 PDFs"),
                html.Li("Complete coverage of all 50 states plus territories"),
            ]
        ),

        html.H3("Data Processing Pipeline", style={"marginTop": "30px"}),
        html.P(
            "The data was retrieved and processed through an innovative LLM-based pipeline:"
        ),
        html.Ol(
            [
                html.Li("Over 3,000 pages of PDFs were retrieved through a web scraper built using Selenium"),
                html.Li("PDFs were converted to PNG format for optimal LLM processing"),
                html.Li("Images were processed through Claude API to create raw CSV files"),
                html.Li("Data was cleaned through multiple iterations of revised prompting"),
                html.Li("Accuracy was evaluated using training and testing datasets (10% sample)"),
                html.Li("Final CSV files were validated and organized by year"),
            ]
        ),

        html.H3("Prompting Parameters", style={"marginTop": "30px"}),
        html.P("Key parameters used in LLM processing:"),
        html.Ul(
            [
                html.Li(html.Strong("System: ") + "Provides context and instructions to Claude"),
                html.Li(html.Strong("Temperature: ") + "Set to 0 for consistent, deterministic output"),
                html.Li(html.Strong("Max tokens: ") + "Controls the length of Claude's output"),
                html.Li(html.Strong("Model: ") + "Claude was selected after comparative testing"),
            ]
        ),

        html.H4("Example Prompt", style={"marginTop": "20px", "marginBottom": "10px"}),
        html.Div(
            style={
                "backgroundColor": "#f8f9fa",
                "padding": "15px",
                "borderRadius": "5px",
                "border": "1px solid #dee2e6",
                "fontFamily": "monospace",
                "fontSize": "14px",
            },
            children=[
                html.P(
                    "I am going to give you an image of some US election data. The goal is to collect "
                    "the following data and provide output in a CSV format: STATE, YEAR, RACE_TYPE, "
                    "CONGRESSIONAL_DISTRICT, CANDIDATE_NAME, CANDIDATE_PARTY, VOTES. Extract the data "
                    "from the image provided and convert it into a CSV format. Include appropriate headers "
                    "based on the content of the image, and return the CSV as plain text.",
                    style={"margin": "0"}
                )
            ]
        ),

        html.H3("Prompting Experiments", style={"marginTop": "30px"}),
        html.P("Key adjustments made during the prompting process:"),
        html.Ul(
            [
                html.Li("Addressed formatting challenges in 1920-1924 data (two-column format)"),
                html.Li("Set temperature to 0 for consistency and faster processing"),
                html.Li("Used system parameters to handle errors and ensure CSV-only output"),
                html.Li("Added specific instructions: 'Write names exactly as they appear, do not try to predict correct spellings'"),
            ]
        ),

        html.H3("LLM Model Comparison: Claude vs ChatGPT", style={"marginTop": "30px"}),
        html.P(
            "We conducted comprehensive testing between Claude (Anthropic) and ChatGPT (OpenAI) "
            "using identical prompts and processing methods."
        ),

        html.H4("Performance Results", style={"marginTop": "20px", "marginBottom": "15px"}),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "gap": "20px",
                "margin": "20px 0",
            },
            children=[
                html.Div(
                    style={
                        "backgroundColor": "#f8f9fa",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "border": "1px solid #dee2e6",
                        "flex": "1",
                    },
                    children=[
                        html.H5(
                            "Claude (Anthropic)",
                            style={
                                "marginBottom": "15px",
                                "color": "#495057",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            [
                                html.Div([html.Strong("State: "), html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})], style={"marginBottom": "8px"}),
                                html.Div([html.Strong("Race Type: "), html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})], style={"marginBottom": "8px"}),
                                html.Div([html.Strong("District: "), html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})], style={"marginBottom": "8px"}),
                                html.Div([html.Strong("Candidate Name: "), html.Span("94%", style={"color": "#fd7e14", "fontWeight": "bold"})], style={"marginBottom": "8px"}),
                                html.Div([html.Strong("Candidate Party: "), html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})], style={"marginBottom": "8px"}),
                                html.Div([html.Strong("Vote Counts: "), html.Span("98%", style={"color": "#28a745", "fontWeight": "bold"})]),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "backgroundColor": "#fff2f2",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "border": "1px solid #f5c6cb",
                        "flex": "1",
                    },
                    children=[
                        html.H5(
                            "ChatGPT (OpenAI)",
                            style={
                                "marginBottom": "15px",
                                "color": "#495057",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            [
                                html.Div([html.Strong("State: "), html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})], style={"marginBottom": "8px"}),
                                html.Div([html.Strong("Race Type: "), html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})], style={"marginBottom": "8px"}),
                                html.Div([html.Strong("District: "), html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})], style={"marginBottom": "8px"}),
                                html.Div([html.Strong("Candidate Name: "), html.Span("70%", style={"color": "#dc3545", "fontWeight": "bold"})], style={"marginBottom": "8px"}),
                                html.Div([html.Strong("Candidate Party: "), html.Span("95%", style={"color": "#fd7e14", "fontWeight": "bold"})], style={"marginBottom": "8px"}),
                                html.Div([html.Strong("Vote Counts: "), html.Span("80%", style={"color": "#dc3545", "fontWeight": "bold"})]),
                            ]
                        ),
                    ],
                ),
            ],
        ),

        html.H4("Key Findings", style={"marginTop": "20px"}),
        html.Ul(
            [
                html.Li([html.Strong("Claude demonstrated superior performance: "), "Significantly outperformed ChatGPT in data collection and OCR tasks"]),
                html.Li([html.Strong("Candidate name accuracy challenges: "), "Achieved 94% accuracy through extensive prompt engineering"]),
                html.Li([html.Strong("ChatGPT limitations: "), "Poor performance on candidate names (70%) and vote counts (80%)"]),
                html.Li([html.Strong("Consistent structured data: "), "Both models performed perfectly on standardized fields"]),
            ]
        ),

        html.H3("Data Quality Assurance", style={"marginTop": "30px"}),
        html.P("Our validation process ensures high-quality, reliable election data:"),
        html.Ul(
            [
                html.Li([html.Strong("Training/Testing Split: "), "10% of data used for accuracy evaluation"]),
                html.Li([html.Strong("Levenshtein Distance Testing: "), "String-based accuracy measurement for text fields"]),
                html.Li([html.Strong("Numerical Accuracy Validation: "), "Custom digit-level accuracy for vote counts"]),
                html.Li([html.Strong("Cross-Model Validation: "), "Comparative testing between Claude and ChatGPT"]),
                html.Li([html.Strong("Final Accuracy: "), "100% accuracy for most variables, 94% for candidate names, 98% for vote counts"]),
            ]
        ),

        html.H3("Data Source", style={"marginTop": "30px"}),
        html.P("All original election results are from the official US House of Representatives archive:"),
        html.A(
            "History, Art, & Archives - US House Election Statistics",
            href="https://history.house.gov/Institution/Election-Statistics/Election-Statistics/",
            target="_blank",
            style={"color": "#0d6efd", "textDecoration": "underline"},
        ),

        html.P(
            "The final CSV files have been pushed to the Open Elections GitHub repository and are accessible through this website.",
            style={"marginTop": "30px", "fontStyle": "italic"},
        ),
    ],
)
