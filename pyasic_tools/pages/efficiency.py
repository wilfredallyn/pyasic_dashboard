import dash
from dash import callback, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from io import StringIO
import json
import pandas as pd
import plotly.graph_objects as go
from pyasic_tools.figs import get_efficiency_fig


dash.register_page(__name__, path="/efficiency", name="Efficiency")


def layout() -> html.Div:
    return html.Div(
        [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dcc.Graph(id="efficiency-graph"),
                        ]
                    )
                ]
            ),
            dcc.Store(id="data-store"),
        ]
    )


@callback(Output("efficiency-graph", "figure"), [Input("data-store", "data")])
def update_efficiency_graph(data: str) -> go.Figure:
    if data is None:
        return {}

    df_json = json.loads(data)
    df = pd.read_json(StringIO(df_json), orient="split")

    fig = get_efficiency_fig(df)
    return fig
