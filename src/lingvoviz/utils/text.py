"""Formatting helpers used across the project."""

from __future__ import annotations


def format_human_number(number: float | int) -> str:
    """Format large counts for the dashboard overview cards."""
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    if number >= 1_000:
        return f"{number / 1_000:.1f}K"
    return str(int(number))
