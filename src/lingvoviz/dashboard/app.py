"""Dash application entrypoint."""

from __future__ import annotations

import os

import dash
import dash_bootstrap_components as dbc

from lingvoviz.config import DEFAULT_HOST, DEFAULT_PORT
from lingvoviz.dashboard.callbacks import register_callbacks
from lingvoviz.dashboard.data import load_dashboard_dataset
from lingvoviz.dashboard.layout import build_layout


def create_app() -> dash.Dash:
    """Create and configure the Dash application."""
    dataframe = load_dashboard_dataset()
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    )
    app.layout = build_layout(dataframe)
    register_callbacks(app, dataframe)
    return app


app = create_app()
server = app.server


if __name__ == "__main__":
    app.run(host=DEFAULT_HOST, port=int(os.environ.get("PORT", DEFAULT_PORT)), debug=False)
