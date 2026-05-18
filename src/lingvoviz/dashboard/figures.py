"""Chart creation for the LingvoViz dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.express as px


STATUS_DESCRIPTIONS = {
    "Not in use": (
        "There are no speakers left.<br>"
        "The language presumably went out of use after 1950."
    ),
    "Severely endangered": (
        "The language has between 10,000 to 100,000 speakers.<br>"
        "It is spoken mostly by grandparents and older generations."
    ),
    "Critically endangered": (
        "The language is spoken by fewer than 25,000 speakers.<br>"
        "The youngest speakers are grandparents and older."
    ),
    "Endangered/unsafe": "The language has from small numbers to 7.5 million speakers.",
    "Definitely endangered": (
        "The language has between 100,000 and 3.5 million speakers.<br>"
        "Children no longer learn it as a mother tongue in the home."
    ),
    "Potentially vulnerable": (
        "The language has between 3.5 million and 7 million speakers.<br>"
        "Children still speak it, but often in restricted domains."
    ),
    "Safe": (
        "The language is spoken by all generations and intergenerational "
        "transmission is uninterrupted."
    ),
}


def build_status_figure(df: pd.DataFrame):
    """Build the vitality status bar chart."""
    status_df = df["Status"].value_counts().reset_index()
    status_df.columns = ["Status", "Count"]
    status_df["Description"] = status_df["Status"].map(STATUS_DESCRIPTIONS)

    figure = px.bar(
        status_df,
        x="Status",
        y="Count",
        title="Languages by vitality",
        hover_data={"Description": True, "Status": False, "Count": False},
        text="Count",
        color="Status",
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    figure.update_traces(hoverlabel={"font_size": 12, "namelength": -1})
    figure.update_layout(
        showlegend=False,
        hovermode="closest",
        margin={"l": 50, "r": 50, "t": 50, "b": 50},
    )
    return figure


def build_family_figure(df: pd.DataFrame):
    """Build the family size vs speakers scatter plot."""
    family_counts = df["Top-level family"].value_counts().reset_index()
    family_counts.columns = ["Top-level family", "Count"]

    family_speakers = df.groupby("Top-level family")["Speakers"].sum().reset_index()
    family_speakers.columns = ["Top-level family", "Total number of speakers"]

    family_summary = pd.merge(family_counts, family_speakers, on="Top-level family")
    family_summary["text"] = family_summary.apply(
        lambda row: (
            f"{row['Top-level family']}\n{row['Count']} languages"
            if row["Count"] > 200
            else ""
        ),
        axis=1,
    )

    figure = px.scatter(
        family_summary,
        x="Count",
        y="Total number of speakers",
        size="Count",
        color="Top-level family",
        hover_name="Top-level family",
        hover_data={
            "Count": False,
            "Top-level family": False,
            "Total number of speakers": True,
        },
        size_max=120,
        text="text",
        title="Language families by number of languages and speakers",
    )
    figure.update_layout(xaxis_title="Number of Languages")
    figure.update_traces(textposition="middle center", textfont_size=10)
    return figure


def build_map_figure(df: pd.DataFrame, search_value: str | None = None):
    """Build the world map, optionally filtered by language name."""
    filtered_df = df
    title = "Languages of the world"

    if search_value:
        filtered_df = df[df["Name"].str.contains(search_value, case=False, na=False)]
        title = f"Languages matching '{search_value}'"

    if filtered_df.empty:
        figure = px.scatter_geo(title=f"No languages found for '{search_value}'")
        figure.update_layout(showlegend=False)
        return figure

    unique_families = filtered_df["Top-level family"].dropna().unique()
    sampled_colors = px.colors.sample_colorscale(
        px.colors.qualitative.Dark24,
        [index / max(len(unique_families), 1) for index in range(len(unique_families))],
    )
    color_mapping = {
        family: color for family, color in zip(unique_families, sampled_colors, strict=False)
    }

    map_df = filtered_df.copy()
    map_df["Speakers"] = map_df["Speakers"].fillna(1)
    map_df["hover_text"] = map_df.apply(
        lambda row: (
            f"Language: {row['Name']}<br>"
            f"Status: {row['Status']}<br>"
            f"Speakers: approx. {row['Speakers']}<br>"
            f"More info: {row['Link']}"
        ),
        axis=1,
    )

    figure = px.scatter_geo(
        map_df,
        lon="Longitude",
        lat="Latitude",
        hover_name="Name",
        hover_data={
            "Name": False,
            "Status": True,
            "Speakers": True,
            "Top-level family": True,
            "Country": True,
            "Link": True,
            "Longitude": False,
            "Latitude": False,
        },
        color="Top-level family",
        projection="natural earth",
        color_discrete_map=color_mapping,
        title=title,
    )
    figure.update_layout(
        geo={
            "projection_type": "natural earth",
            "showland": True,
            "landcolor": "lightgray",
        },
        showlegend=False,
    )
    return figure
