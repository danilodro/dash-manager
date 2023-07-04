import dash_bootstrap_components as dbc

from dash import html

PLOTLY_LOGO = "https://cdnb.artstation.com/p/assets/images/images/045/524/453/large/hithan-estudio-3d-01.jpg?1642944021"

layout = [
    html.H2(
        "Bem-vindo(a) ao IntelDash!",
        className="display-5",
        style={"textAlign": "center"},
    ),
    html.Hr(),
    dbc.Col(
        html.Img(
            src=PLOTLY_LOGO,
            style={"width": "100%", "height": "100%"},
        )
    ),
]
