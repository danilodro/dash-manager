import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from src.components.Table import create_table_component

from dash import dcc, html

TEXT_COLOR = "#424749"


def create_card_component(encoded_csv, table, header_title, name_file):
    return dbc.Container(
        children=[
            dbc.Card(
                dbc.CardBody(
                    children=[
                        dbc.CardHeader(
                            children=[
                                html.Div(
                                    children=[
                                        html.H5(
                                            header_title,
                                            style={
                                                "color": TEXT_COLOR,
                                                "font-family": "System-ui",
                                            },
                                        ),
                                        dmc.ThemeIcon(
                                            size="lg",
                                            color="green",
                                            variant="light",
                                            radius="sm",
                                            children=[
                                                html.A(
                                                    DashIconify(
                                                        icon="feather:download",
                                                        width=25,
                                                    ),
                                                    href="data:text/csv;charset=utf-8;base64,"
                                                    + encoded_csv,
                                                    download=name_file,
                                                    target="_blank",
                                                ),
                                            ],
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flex-direction": "row",
                                        "justify-content": "space-between",
                                        "vertical-align": "middle",
                                    },
                                ),
                            ],
                            style={},
                        ),
                        create_table_component(table)
                    ],
                    style={"padding": "0px"},
                ),
            )
        ],
        fluid=True,
        style={
            "padding-top": "10px",
            "padding-bottom": "10px",
            "padding-left": "0px",
            "padding-right": "0px",
        },
    )
