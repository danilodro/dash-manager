import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dash import Dash, Input, Output, html

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
)


def get_icon(icon):
    return DashIconify(icon=icon, height=16)


app.layout = html.Div(
    style={"width": 240},
    children=[
        dmc.NavLink(
            label="First parent link",
            icon=get_icon(icon="tabler:gauge"),
            childrenOffset=28,
            id="teste",
            children=[
                dmc.NavLink(label="First child link"),
                dmc.NavLink(label="Second child link"),
                dmc.NavLink(
                    label="Nested parent link",
                    childrenOffset=28,
                    children=[
                        dmc.NavLink(label="First child link"),
                        dmc.NavLink(label="Second child link"),
                        dmc.NavLink(label="Third child link"),
                    ],
                ),
            ],
        ),
        dmc.NavLink(
            id="teste",
            label="Second parent link",
            icon=get_icon(icon="tabler:fingerprint"),
        ),
        dmc.NavLink(
            label="Second parent link",
            icon=get_icon(icon="tabler:fingerprint"),
            childrenOffset=28,
            opened=False,
            id="teste",
            children=[
                dmc.NavLink(id="navlink-child", label="First child link"),
                dmc.NavLink(label="Second child link"),
                dmc.NavLink(label="Third child link"),
            ],
        ),
    ],
)


@app.callback(Output("teste", "style"), Input("teste", "n_clicks"))
def change_style(opened):
    print(opened % 2)
    if opened and opened % 2:
        return {"color": "#fff", "border-radius": "10px", "background": "#FF5733"}
    return {}


app.run_server(debug=True)
