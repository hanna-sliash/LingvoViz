"""Dash callbacks."""

from __future__ import annotations

import pandas as pd
from dash import Dash, Input, Output, State, dcc

from lingvoviz.dashboard.figures import build_map_figure
from lingvoviz.dashboard.layout import build_overview_card
from lingvoviz.dashboard.figures import build_family_figure, build_status_figure


def register_callbacks(app: Dash, df: pd.DataFrame) -> None:
    """Register all app callbacks."""

    @app.callback(
        Output("map-plot", "figure"),
        Input("search-button", "n_clicks"),
        Input("search-bar", "n_submit"),
        State("search-bar", "value"),
    )
    def update_map(_button_clicks: int, _submit_count: int, search_value: str | None):
        return build_map_figure(df, search_value=search_value)

    @app.callback(
        Output("insight-panel", "children"),
        Input("insight-selector", "value"),
    )
    def update_insight_panel(selected_view: str):
        if selected_view == "vitality":
            return dcc.Graph(
                id="status-figure",
                figure=build_status_figure(df),
                style={"height": "460px"},
            )

        if selected_view == "families":
            return dcc.Graph(
                id="family-figure",
                figure=build_family_figure(df),
                style={"height": "500px"},
            )

        return build_overview_card(df)
