import base64

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash_iconify import DashIconify

from dash import Dash, Input, Output, State, callback
from dash import callback_context as ctx
from dash import dcc, html, no_update
from src.Blip.Blip import Blip
from src.components.BarChart import create_bar_chart
from src.components.Card import create_card_component
from src.http.BlipHttp import BlipRequest
from src.pages import attendance_report, home
from src.utils.format_time import format_time

app = Dash(
    external_stylesheets=[dbc.themes.MINTY, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

TEXT_COLOR = "#424749"

blip_http = BlipRequest("Key YXRlbmRpbWVudG9odW1hbm8xMzM6RUVsWjFtV0ZTV1ZnVDQ1Z2VQY2w=")

sidebar = html.Div(
    [
        html.Div(
            html.Img(
                src=r"assets\intel-dash.png",
                className="logo-image",
                style={
                    "width": "100%",
                    "height": "auto",
                    "display": "block",
                    "margin-left": "auto",
                    "margin-right": "auto",
                },
            ),
            className="logo-container",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    "Home", href="/", active="exact", style={"color": TEXT_COLOR}
                ),
                dbc.NavLink(
                    "Relatório de atendimento",
                    href="/relatorio-de-atendimento",
                    active="exact",
                    style={"color": TEXT_COLOR},
                ),
                dbc.NavLink(
                    "Gerenciamento",
                    href="/gerenciamento",
                    active="exact",
                    style={"color": TEXT_COLOR},
                ),
            ],
            vertical=True,
            pills=True,
            id="nav-bar",
        ),
    ],
    id="side-bar",
)

content = html.Div(
    id="page-content",
)

app.layout = html.Div(
    [dcc.Location(id="url"), sidebar, content],
)


@app.callback(
    Output("dropdown-values", "data"),
    Input("dropdown-teams", "value"),
)
def save_options(dropdown_value):
    if dropdown_value is not None:
        return dropdown_value
    return []


@app.callback(
    Output("output-content", "children"),
    Input("date-picker", "value"),
    Input("dropdown-values", "data"),
    Input("dropdown-teams", "value"),
)
def update_output(dates, queues, dropdown_selection):
    if dates and len(dates) > 1:
        start_date, end_date = dates
        productivity_agents = blip_http.get_agents_productivity(start_date, end_date)[
            "resource"
        ]["items"]

        report_teams = blip_http.get_report_about_teams(start_date, end_date)[
            "resource"
        ]["items"]

        data = {"filas": [], "total": []}

        if queues:
            teams_filter = []

            for item in report_teams:
                if item["name"] in queues:
                    teams_filter.append(item)

            report_teams = teams_filter

        for item in report_teams:
            data["filas"].append(item["name"])
            data["total"].append(item["ticketsCount"])

            item["averageWaitTime"] = item["averageWaitTime"].split(".")[0]
            item["averageTalkTime"] = item["averageTalkTime"].split(".")[0]

        df = pd.DataFrame(data)

        return html.Div(
            children=[
                create_card_component(
                    "Total de atendimentos",
                    str(df["total"].sum()),
                    "fas fa-calendar-check",
                ),
                create_card_component(
                    "Tempo médio de espera",
                    format_time(sum(df["averageWaitTime"])),
                    "fas fa-stopwatch",
                ),
                create_card_component(
                    "Tempo médio de atendimento",
                    format_time(sum(df["averageTalkTime"])),
                    "fas fa-users",
                ),
                html.Hr(),
                dcc.Graph(
                    id="bar-chart",
                    figure=create_bar_chart(df, "filas", "total"),
                    config={"displayModeBar": False},
                ),
            ],
            className="cards-container",
        )

    return []


@app.callback(
    Output("output", "children"),
    Input("dropdown-teams", "value"),
    Input("date-picker", "value"),
    State("dropdown-values", "data"),
    prevent_initial_call=True,
)
def create_chatbot(queues, date_range, dropdown_values):
    if not queues or not date_range:
        return []

    start_date, end_date = date_range

    chatbots = []
    chart = go.Figure()

    for queue in queues:
        report = blip_http.get_report_by_queue(queue, start_date, end_date)

        if "items" in report["resource"]:
            chatbot = Blip()

            chatbot.set_property("queue_name", queue)
            chatbot.set_property("start_date", start_date)
            chatbot.set_property("end_date", end_date)
            chatbot.set_property("date_range", date_range)

            chatbot.consume_queue(report)
            chatbot.generate_report()
            chatbots.append(chatbot)

            chart.add_trace(
                go.Bar(
                    x=[queue],
                    y=[chatbot.get_total_tickets()],
                    name="Total de atendimentos",
                    marker_color="#16a085",
                )
            )

    if not chatbots:
        return html.Div(
            html.H3("Não há dados para exibir.", style={"text-align": "center"})
        )

    chart.update_layout(
        yaxis=dict(title="Quantidade de atendimentos"),
        xaxis=dict(title="Fila de atendimento"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font_color=TEXT_COLOR,
    )

    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Graph(
                        id="bar-chart",
                        figure=chart,
                        config={"displayModeBar": False},
                    ),
                ],
                className="graph-container",
            ),
            html.Hr(),
            html.Div(
                children=[
                    dbc.Button(
                        "Gerar relatório de atendimento",
                        id="button-create-report",
                        color="primary",
                        className="button-report",
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Relatório de atendimento"),
                            dbc.ModalBody(
                                html.P(
                                    "O relatório será gerado e enviado para o seu e-mail."
                                )
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Fechar",
                                    id="button-close-report-modal",
                                    className="ml-auto",
                                )
                            ),
                        ],
                        id="modal-report",
                    ),
                ],
                className="button-container",
            ),
        ],
        className="chatbot-container",
    )


@app.callback(
    Output("modal-report", "is_open"),
    Output("modal-report", "children"),
    Input("button-create-report", "n_clicks"),
    State("button-close-report-modal", "n_clicks"),
    State("dropdown-teams", "value"),
    State("date-picker", "value"),
    State("dropdown-values", "data"),
    prevent_initial_call=True,
)
def create_report(n_clicks, close_modal, queues, date_range, dropdown_values):
    if not queues or not date_range:
        return False, []

    if n_clicks and n_clicks > 0:
        start_date, end_date = date_range

        blip_http.create_report_email(queues, start_date, end_date)

        return True, [
            dbc.ModalHeader("Relatório de atendimento"),
            dbc.ModalBody(
                html.P("O relatório está sendo gerado e será enviado para o seu e-mail.")
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Fechar",
                    id="button-close-report-modal",
                    className="ml-auto",
                )
            ),
        ]

    return False, []


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def render_page_content(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/relatorio-de-atendimento":
        return attendance_report.layout
    else:
        return home.layout


if __name__ == "__main__":
    app.run_server(debug=True)

