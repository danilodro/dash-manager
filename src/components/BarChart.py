import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dash import dcc, html

TEXT_COLOR = "#424749"


def create_bar_chart(bar_chart, header_title, graph_id):
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
                        dcc.Graph(
                            figure=bar_chart,
                            id=graph_id,
                            config={"displayModeBar": False},
                        ),
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
