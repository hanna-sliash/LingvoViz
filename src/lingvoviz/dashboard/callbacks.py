"""Dash callbacks."""

from __future__ import annotations

import pandas as pd
from dash import Dash, Input, Output, State

from lingvoviz.dashboard.figures import build_map_figure


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
