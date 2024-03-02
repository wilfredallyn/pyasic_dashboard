import dash
from dash import callback, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from io import StringIO
import json
import pandas as pd
import plotly.graph_objects as go
from pyasic_dashboard.figs import get_temperature_fig


dash.register_page(__name__, path="/temperature", name="Temperature")


def layout() -> html.Div:
    return html.Div(
        [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dcc.Graph(id="temperature-graph"),
                        ]
                    )
                ]
            ),
            dcc.Store(id="data-store"),
        ]
    )


@callback(Output("temperature-graph", "figure"), [Input("data-store", "data")])
def update_temperature_graph(data: str) -> go.Figure:
    if data is None:
        return {}

    df_json = json.loads(data)
    df = pd.read_json(StringIO(df_json), orient="split")

    fig = get_temperature_fig(df)
    return fig
