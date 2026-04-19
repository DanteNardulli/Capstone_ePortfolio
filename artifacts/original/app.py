"""Enhanced Dash application for the Grazioso Salvare rescue dashboard.

Enhancement One focuses on software design and engineering by moving query
construction and DataFrame preparation into reusable service functions.
"""

from __future__ import annotations

import base64
from pathlib import Path

import dash_leaflet as dl
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dash_table, dcc, html

from crud import AnimalShelter
from query_service import build_rescue_query, prepare_dataframe

APP_TITLE = "Dashboard by Dante Nardulli - CS340 Project Two"
LOGO_PATH = Path(__file__).with_name("grazioso_logo.png")
DEFAULT_CENTER = [30.75, -97.48]


def load_logo() -> str:
    """Return the Grazioso Salvare logo as a base64 string for the layout."""
    if not LOGO_PATH.exists():
        return ""
    return base64.b64encode(LOGO_PATH.read_bytes()).decode()


try:
    database = AnimalShelter()
    initial_df = prepare_dataframe(database.read())
except ConnectionError:
    database = None
    initial_df = pd.DataFrame()

app = Dash(__name__)
encoded_logo = load_logo()

app.layout = html.Div(
    [
        html.Img(
            src=f"data:image/png;base64,{encoded_logo}" if encoded_logo else "",
            style={"height": "100px"},
        ),
        html.H4(APP_TITLE, style={"textAlign": "center"}),
        html.Center(html.B(html.H1("CS-340 Dashboard"))),
        html.Hr(),
        dcc.RadioItems(
            id="filter-type",
            options=[
                {"label": "All Dogs", "value": "all"},
                {"label": "Water Rescue", "value": "water"},
                {"label": "Mountain or Wilderness Rescue", "value": "mountain"},
                {"label": "Disaster or Individual Tracking", "value": "disaster"},
            ],
            value="all",
            labelStyle={"display": "inline-block", "margin": "10px"},
        ),
        html.Hr(),
        dash_table.DataTable(
            id="datatable-id",
            columns=[
                {"name": column_name, "id": column_name, "deletable": False, "selectable": True}
                for column_name in initial_df.columns
            ],
            data=initial_df.to_dict("records"),
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="single",
            row_deletable=False,
            selected_rows=[0],
            page_action="native",
            page_current=0,
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={
                "minWidth": "150px",
                "width": "150px",
                "maxWidth": "150px",
                "whiteSpace": "normal",
            },
        ),
        html.Br(),
        html.Hr(),
        html.Div(
            className="row",
            style={"display": "flex"},
            children=[
                html.Div(id="graph-id", className="col s12 m6"),
                html.Div(id="map-id", className="col s12 m6"),
            ],
        ),
    ]
)


@app.callback(Output("datatable-id", "data"), Input("filter-type", "value"))
def update_dashboard(filter_type: str) -> list[dict]:
    """Refresh the table based on the selected rescue category."""
    if database is None:
        return []
    query = build_rescue_query(filter_type)
    return prepare_dataframe(database.read(query)).to_dict("records")


@app.callback(Output("graph-id", "children"), Input("datatable-id", "derived_virtual_data"))
def update_graphs(view_data: list[dict] | None):
    """Render a pie chart for the currently visible records."""
    if not view_data:
        return html.Div("No data available to generate chart.")

    dataframe = pd.DataFrame(view_data)
    if "breed" not in dataframe.columns:
        return html.Div("Column 'breed' not found in data.")

    figure = px.pie(dataframe, names="breed", title="Breed Distribution")
    return dcc.Graph(figure=figure)


@app.callback(Output("datatable-id", "style_data_conditional"), Input("datatable-id", "selected_columns"))
def update_styles(selected_columns: list[str] | None) -> list[dict]:
    """Highlight the selected column in the data table."""
    if not selected_columns:
        return []
    return [
        {"if": {"column_id": column_name}, "backgroundColor": "#D2F3FF"}
        for column_name in selected_columns
    ]


@app.callback(
    Output("map-id", "children"),
    Input("datatable-id", "derived_virtual_data"),
    Input("datatable-id", "derived_virtual_selected_rows"),
)
def update_map(view_data: list[dict] | None, index: list[int] | None):
    """Display the map marker for the selected animal record."""
    if not view_data:
        return html.Div("No location data available.")

    dataframe = pd.DataFrame.from_dict(view_data)
    row_index = index[0] if index else 0

    if dataframe.empty or row_index >= len(dataframe.index):
        return html.Div("No location data available.")

    required_columns = {"location_lat", "location_long", "breed", "name"}
    if not required_columns.issubset(dataframe.columns):
        return html.Div("Location data is missing for the selected record.")

    row = dataframe.iloc[row_index]
    return [
        dl.Map(
            style={"width": "1000px", "height": "500px"},
            center=DEFAULT_CENTER,
            zoom=10,
            children=[
                dl.TileLayer(id="base-layer-id"),
                dl.Marker(
                    position=[row["location_lat"], row["location_long"]],
                    children=[
                        dl.Tooltip(row["breed"]),
                        dl.Popup([html.H1("Animal Name"), html.P(row.get("name", "Unknown"))]),
                    ],
                ),
            ],
        )
    ]


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
