import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dash import Dash, Input, Output, callback, html

app = Dash(
    suppress_callback_exceptions=True,
)

app.layout = dmc.NotificationsProvider(
    html.Div(
        [
            html.Div(id="notifications-container"),
            dmc.Button("Show Notification", id="notify"),
        ]
    )
)


@callback(
    Output("notifications-container", "children"),
    Input("notify", "n_clicks"),
    prevent_initial_call=True,
)
def show(n_clicks):
    return dmc.Notification(
        title="Hey there!",
        id="simple-notify",
        action="show",
        message="Notifications in Dash, Awesome!",
        icon=DashIconify(icon="ic:round-celebration"),
    )


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
