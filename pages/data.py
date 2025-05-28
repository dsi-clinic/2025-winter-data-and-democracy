"""Data page layout displaying available datasets and processing information."""
from dash import html

layout = html.Div(
    style={"padding": "40px", "maxWidth": "900px", "margin": "auto"},
    children=[
        html.H2("Available Datasets", style={"fontWeight": "bold"}),
        html.P(
            "Below you'll find our processed election data in machine-readable formats, "
            "created using Large Language Models to extract data from historical PDF documents."
        ),
        
        html.H3("Data Overview", style={"marginTop": "30px"}),
        html.P(
            "Our dataset contains comprehensive federal election results from 1920 to 1996, "
            "processed from archival PDF documents using advanced LLM technology to create "
            "accurate, machine-readable CSV files."
        ),
        
        html.H3("Data Coverage", style={"marginTop": "30px"}),
        html.Ul([
            html.Li("51 PDFs totaling 3,000+ pages of archival election data"),
            html.Li("Federal-level elections from 1920 to 1996"),
            html.Li("House, Senate, and Presidential election results"),
            html.Li("Vote counts for every party and candidate"),
            html.Li("Complete coverage of all 50 states plus territories"),
        ]),

        html.H3("Data Source", style={"marginTop": "30px"}),
        html.P(
            "All data was sourced from the official US House Election Statistics archive, "
            "providing authoritative historical election information directly from government records."
        ),
        html.A(
            "US House Election Statistics (Primary Source)",
            href="https://history.house.gov/Institution/Election-Statistics/Election-Statistics/",
            target="_blank",
            style={"color": "#0d6efd", "textDecoration": "underline"},
        ),

        html.H3("Data Format", style={"marginTop": "30px"}),
        html.P(
            "Our data follows standardized specifications containing the following variables: "
            "year, state, candidate name, candidate party, district (for house races), and votes. "
            "All data is available as downloadable CSV files."
        ),

        html.H3("LLM Data Processing Pipeline", style={"marginTop": "30px"}),
        html.P(
            "Our innovative pipeline leverages Large Language Models to accurately extract data "
            "from historical PDF documents:"
        ),
        html.Ul(
            [
                html.Li("3,000+ PDF pages scraped from the US House Election Statistics archive"),
                html.Li("PDFs converted to PNG images for optimal LLM processing"),
                html.Li("Advanced prompt engineering to ensure complete variable extraction"),
                html.Li("Systematic testing of prompting parameters: system prompts, temperature, max tokens, and model selection"),
                html.Li("Regular expression preprocessing for data noise reduction and post-processing for corrections"),
                html.Li("Rigorous accuracy validation using Levenshtein distance for text and digit-level comparison for numbers"),
            ]
        ),

        html.H3("LLM Model Comparison: Claude vs ChatGPT", style={"marginTop": "30px"}),
        html.P(
            "We conducted comprehensive testing between Claude (Anthropic) and ChatGPT (OpenAI) "
            "to determine the optimal model for election data extraction. Using identical prompts "
            "and processing methods, we evaluated performance across all data fields using edit "
            "distance tests for text values and numerical accuracy tests for vote counts."
        ),
        
        html.H4("Performance Results", style={"marginTop": "20px", "marginBottom": "15px"}),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "gap": "20px",
                "margin": "20px 0"
            },
            children=[
                html.Div(
                    style={
                        "backgroundColor": "#f8f9fa",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "border": "1px solid #dee2e6",
                        "flex": "1"
                    },
                    children=[
                        html.H5("Claude (Anthropic)", style={"marginBottom": "15px", "color": "#495057", "textAlign": "center"}),
                        html.Div([
                            html.Div([
                                html.Strong("State: "),
                                html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})
                            ], style={"marginBottom": "8px"}),
                            html.Div([
                                html.Strong("Race Type: "),
                                html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})
                            ], style={"marginBottom": "8px"}),
                            html.Div([
                                html.Strong("District: "),
                                html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})
                            ], style={"marginBottom": "8px"}),
                            html.Div([
                                html.Strong("Candidate Name: "),
                                html.Span("94%", style={"color": "#fd7e14", "fontWeight": "bold"})
                            ], style={"marginBottom": "8px"}),
                            html.Div([
                                html.Strong("Candidate Party: "),
                                html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})
                            ], style={"marginBottom": "8px"}),
                            html.Div([
                                html.Strong("Vote Counts: "),
                                html.Span("98%", style={"color": "#28a745", "fontWeight": "bold"})
                            ]),
                        ])
                    ]
                ),
                html.Div(
                    style={
                        "backgroundColor": "#fff2f2",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "border": "1px solid #f5c6cb",
                        "flex": "1"
                    },
                    children=[
                        html.H5("ChatGPT (OpenAI)", style={"marginBottom": "15px", "color": "#495057", "textAlign": "center"}),
                        html.Div([
                            html.Div([
                                html.Strong("State: "),
                                html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})
                            ], style={"marginBottom": "8px"}),
                            html.Div([
                                html.Strong("Race Type: "),
                                html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})
                            ], style={"marginBottom": "8px"}),
                            html.Div([
                                html.Strong("District: "),
                                html.Span("100%", style={"color": "#28a745", "fontWeight": "bold"})
                            ], style={"marginBottom": "8px"}),
                            html.Div([
                                html.Strong("Candidate Name: "),
                                html.Span("70%", style={"color": "#dc3545", "fontWeight": "bold"})
                            ], style={"marginBottom": "8px"}),
                            html.Div([
                                html.Strong("Candidate Party: "),
                                html.Span("95%", style={"color": "#fd7e14", "fontWeight": "bold"})
                            ], style={"marginBottom": "8px"}),
                            html.Div([
                                html.Strong("Vote Counts: "),
                                html.Span("80%", style={"color": "#dc3545", "fontWeight": "bold"})
                            ]),
                        ])
                    ]
                )
            ]
        ),

        html.H4("Key Findings", style={"marginTop": "20px"}),
        html.Ul([
            html.Li(html.Strong("Claude demonstrated superior performance: ") + "Significantly outperformed ChatGPT in data collection and OCR tasks, particularly for complex fields like candidate names and vote counts"),
            html.Li(html.Strong("Candidate name accuracy challenges: ") + "Initially faced difficulties with candidate name recognition due to variability and length, but achieved 94% accuracy through extensive prompt engineering"),
            html.Li(html.Strong("ChatGPT limitations: ") + "Provided unsatisfactory results for diverse entries, with particularly poor performance on candidate names (70%) and vote counts (80%)"),
            html.Li(html.Strong("Consistent structured data: ") + "Both models performed perfectly on standardized fields (State, Race Type, District), but Claude excelled in variable content extraction"),
        ]),

        html.H3("Data Quality Assurance", style={"marginTop": "30px"}),
        html.P("Our validation process ensures high-quality, reliable election data:"),
        html.Ul([
            html.Li(html.Strong("Levenshtein Distance Testing: ") + "String-based accuracy measurement for text fields"),
            html.Li(html.Strong("Numerical Accuracy Validation: ") + "Digit-level comparison for vote count precision"),
            html.Li(html.Strong("Cross-Model Validation: ") + "Comparative testing between multiple LLM models"),
            html.Li(html.Strong("Manual Quality Checks: ") + "Human verification of complex cases and edge scenarios"),
        ]),

        html.P(
            "All CSV files have been processed using our validated Claude-based pipeline and are "
            "available for download and analysis.",
            style={"marginTop": "30px", "fontStyle": "italic"}
        ),
    ],
)
