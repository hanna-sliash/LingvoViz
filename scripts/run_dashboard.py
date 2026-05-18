"""Run the Dash dashboard locally."""

from __future__ import annotations

import os

from _bootstrap import bootstrap

bootstrap()

from lingvoviz.config import DEFAULT_HOST, DEFAULT_PORT
from lingvoviz.dashboard.app import app


if __name__ == "__main__":
    app.run(host=DEFAULT_HOST, port=int(os.environ.get("PORT", DEFAULT_PORT)), debug=False)
