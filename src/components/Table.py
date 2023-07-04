import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dash import dash_table, dcc, html

TEXT_COLOR = "#424749"


def create_table_component(data_table):
    return html.Div(
        children=[
            dash_table.DataTable(
                data=data_table.to_dict("records"),
                columns=[{"name": i, "id": i} for i in data_table.columns],
                page_size=10,
                fixed_rows={"headers": True},
                page_action="none",
                style_table={
                    "height": "300px",
                    "overflowY": "auto",
                    "overflowX": "auto",
                    "padding": "10px",
                    "minWidth": "100%",
                },
                style_cell={
                    "textAlign": "center",
                    "padding": "5px",
                    "color": "#424749",
                },
                style_data_conditional=[
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "#f8f9fa",
                    }
                ],
                style_header={
                    "backgroundColor": "#00A75D",
                    "fontWeight": "bold",
                    "color": "#424749",
                    "whiteSpace": "normal",
                },
                sort_action="native",
                filter_action="native",
                filter_options={
                    "placeholder_text": "Filtrar",
                },
                style_data={
                    "whiteSpace": "normal",
                    "minWidth": "180px",
                    "width": "180px",
                    "maxWidth": "380px",
                    "height": "auto",
                },
            ),
        ],
        style={
            "border-radius": "40px",
            "overflow": "hidden",
        },
    )
