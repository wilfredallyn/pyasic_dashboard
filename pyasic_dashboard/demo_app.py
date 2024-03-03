import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
from flask import Flask
import json
import os
import pandas as pd
from pyasic_dashboard.db import load_db
import sys


dotenv_path = os.path.join(os.getcwd(), os.getenv("ENV_FILE", ".env.dev"))
load_dotenv(dotenv_path=dotenv_path, override=True)

APP_HOST = os.environ.get("HOST")
APP_PORT = int(os.environ.get("PORT", "8050"))
APP_DEBUG = bool(os.environ.get("DEBUG"))
DEV_TOOLS_PROPS_CHECK = bool(os.environ.get("DEV_TOOLS_PROPS_CHECK"))
API_KEY = os.environ.get("API_KEY", None)


server = Flask(__name__)


app = dash.Dash(
    __name__,
    server=server,
    use_pages=True,
    external_stylesheets=[dbc.themes.SPACELAB],
    suppress_callback_exceptions=True,
    title="Pyasic Tools",
)

page_order = ["Status", "Hashrate", "Temperature"]
ordered_pages = sorted(
    dash.page_registry.values(), key=lambda page: page_order.index(page["name"])
)


sidebar = dbc.Nav(
    [
        dbc.NavLink(
            html.Div(page["name"], className="ms-2"), href=page["path"], active="exact"
        )
        for page in ordered_pages
    ],
    vertical=True,
    pills=True,
    className="bg-light",
)

app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        "pyasic tools",
                        style={"fontSize": 50, "textAlign": "center"},
                    )
                )
            ]
        ),
        html.Hr(),
        html.Div(
            [
                "This is a ",
                html.A(
                    " demo app ",
                    href="https://github.com/wilfredallyn/pyasic-tools",
                    target="_blank",
                ),
                " for visualizing ",
                html.A(
                    "pyasic ",
                    href="https://github.com/UpstreamData/pyasic",
                    target="_blank",
                ),
                "data",
            ],
            style={"textAlign": "center"},
        ),
        dbc.Row(
            [
                dbc.Col([sidebar], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
                dbc.Col([dash.page_container], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10),
            ]
        ),
        dcc.Store(id="data-store", storage_type="session"),
    ],
    fluid=True,
)
server = app.server


@app.callback(Output("data-store", "data"), [Input("url", "pathname")])
def load_data(pathname: str) -> str:
    db_file = os.getenv("DEMO_DB_FILE", "../examples/change_power.db")
    df = load_db(db_file, table_name="data")
    # json serialize for dcc.store
    return json.dumps(df.to_json(orient="split"))


if __name__ == "__main__":
    app.run_server(
        host=APP_HOST,
        port=APP_PORT,
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK,
    )
