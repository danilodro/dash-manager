from datetime import datetime, timedelta

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dash import dcc, html
from src.http.BlipHttp import BlipRequest

TEXT_COLOR = "#424749"

blip_http = BlipRequest("Key YXRlbmRpbWVudG9odW1hbm8xMzM6RUVsWjFtV0ZTV1ZnVDQ1Z2VQY2w=")

teams = blip_http.get_teams()
teams_name = []
for team in teams["resource"]["items"]:
    teams_name.append(team["name"])

layout = dbc.Container(
    id="container-report-attendance",
    fluid=True,
    children=[
        html.P(
            "Relatório de atendimento",
            className="display-5",
            style={"color": TEXT_COLOR},
        ),
        dmc.Tooltip(
            label="Selecione uma fila e/ou um periodo para visualizar as informações relacionadas.",
            transition="fade",
            position="right",
            transitionDuration=300,
            children=[
                html.Div(
                    children=[
                        html.Span("Filtrar por: Fila ", className="mr-2 align-middle"),
                        dmc.ThemeIcon(
                            size="sm",
                            color="yellow",
                            variant="light",
                            radius="xl",
                            children=DashIconify(
                                icon="feather:alert-triangle", width=25
                            ),
                            style={"vertical-align": "middle"},
                        ),
                    ]
                )
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dmc.MultiSelect(
                        data=[team for team in teams_name],
                        searchable=True,
                        nothingFound="Fila não encontrada",
                        id="dropdown-teams",
                        style={"width": "100%"},
                        clearable=True,
                        placeholder="Selecione uma ou mais filas",
                    ),
                    width=8,
                ),
                dbc.Col(
                    dmc.DateRangePicker(
                        id="date-picker",
                        # minDate=date(2020, 8, 5),
                        value=[
                            datetime.now().date() - timedelta(days=5),
                            datetime.now().date(),
                        ],
                        style={"width": "100%"},
                        inputFormat="DD/MM/YYYY",
                        allowSingleDateInRange=True,
                        clearable=False,
                    ),
                    width=4,
                ),
            ],
            className="my-2",
            style={"align-items": "center", "display": "flex", "flex-direction": "row"},
        ),
        html.Div(id="output-content"),
        dcc.Store(id="dropdown-values"),
    ],
)
