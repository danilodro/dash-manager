# Import packages
import pandas as pd
import plotly.express as px

from dash import Dash, Input, Output, callback, dash_table, dcc, html

# Incorporate data
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    [
        html.Div(children="My First App with Data, Graph and Controls"),
        html.Hr(),
        dash_table.DataTable(data=df.to_dict("records"), page_size=6),
        dcc.RadioItems(
            options=["pop", "lifeExp", "gdpPercap"],
            value="lifeExp",
            id="controls-and-radio-item",
        ),
        dcc.Graph(figure={}, id="controls-and-graph"),
    ]
)


# Add controls to build the interaction
@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def update_graph(col_chosen):
    fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
