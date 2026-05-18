"""Dashboard layout construction."""

from __future__ import annotations

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html

from lingvoviz.config import DASHBOARD_TITLE
from lingvoviz.dashboard.figures import build_family_figure, build_map_figure, build_status_figure
from lingvoviz.utils.text import format_human_number


def build_overview_card(df: pd.DataFrame) -> dbc.Card:
    """Create the overview summary card."""
    status_counts = df["Status"].value_counts()
    total_languages = int(status_counts.sum())
    safe_languages = df[df["Status"] == "Safe"]["Name"].nunique()
    endangered_languages = df[df["Status"] != "Safe"]["Name"].nunique()
    lost_languages = df[df["Status"] == "Not in use"]["Name"].nunique()

    return dbc.Card(
        [
            dbc.CardHeader("Overview"),
            dbc.CardBody(
                [
                    html.P(
                        [
                            "There are ",
                            html.Span(
                                format_human_number(total_languages),
                                style={
                                    "fontSize": "20px",
                                    "fontWeight": "bold",
                                    "color": "#1f77b4",
                                },
                            ),
                            " languages in the world.",
                        ]
                    ),
                    html.P(
                        [
                            "Only ",
                            html.Span(
                                format_human_number(safe_languages),
                                style={
                                    "fontSize": "20px",
                                    "fontWeight": "bold",
                                    "color": "#1f77b4",
                                },
                            ),
                            " languages are considered safe.",
                        ]
                    ),
                    html.P(
                        [
                            html.Span(
                                format_human_number(endangered_languages),
                                style={
                                    "fontSize": "20px",
                                    "fontWeight": "bold",
                                    "color": "#1f77b4",
                                },
                            ),
                            " languages are vulnerable or endangered.",
                        ]
                    ),
                    html.P(
                        [
                            html.Span(
                                format_human_number(lost_languages),
                                style={
                                    "fontSize": "20px",
                                    "fontWeight": "bold",
                                    "color": "#1f77b4",
                                },
                            ),
                            " languages are no longer in use.",
                        ]
                    ),
                ]
            ),
        ],
        style={"marginBottom": "10px", "padding": "10px"},
    )


def build_layout(df: pd.DataFrame) -> dbc.Container:
    """Create the Dash layout for the dashboard."""
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H1(
                            DASHBOARD_TITLE,
                            className="text-center text-primary mb-4",
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.H3(
                            (
                                "This dashboard explores global language diversity. "
                                "Use the charts and map to compare language vitality, "
                                "families, and geographic distribution."
                            ),
                            className="text-secondary",
                            style={"textAlign": "left"},
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            build_overview_card(df),
                            dcc.Graph(
                                id="status-figure",
                                figure=build_status_figure(df),
                                style={"height": "400px"},
                            ),
                            dcc.Graph(
                                id="family-figure",
                                figure=build_family_figure(df),
                                style={"height": "420px"},
                            ),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Input(
                                            id="search-bar",
                                            type="text",
                                            placeholder="Search for a language",
                                            debounce=True,
                                            style={"width": "100%"},
                                        ),
                                        width=8,
                                    ),
                                    dbc.Col(
                                        html.Button(
                                            "Search",
                                            id="search-button",
                                            n_clicks=0,
                                            className="btn btn-primary",
                                        ),
                                        width="auto",
                                    ),
                                ],
                                justify="center",
                                style={"marginBottom": "10px"},
                            ),
                            dcc.Graph(
                                id="map-plot",
                                figure=build_map_figure(df),
                                style={"height": "75vh"},
                            ),
                        ],
                        width=8,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Footer(
                            (
                                "Data sources: UNESCO World Atlas of Languages and "
                                "Glottolog 5.1 edited by Harald Hammarstrom, "
                                "Robert Forkel, Martin Haspelmath, and Sebastian Bank."
                            ),
                            style={
                                "textAlign": "left",
                                "padding": "10px",
                                "color": "gray",
                                "fontSize": 12,
                            },
                        )
                    )
                ]
            ),
        ],
        fluid=True,
    )
