import dash
from dash import callback, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


dash.register_page(__name__, path="/control", name="Control")


def layout() -> html.Div:
    return html.Div(
        [
            dcc.Input(
                id="time",
                type="text",
                placeholder="Time (e.g., 1600 for 4PM)",
            ),
            dcc.Input(id="power-level", type="text", placeholder="Power (e.g., 1000)"),
            html.Button("Add Power Change", id="add-button", n_clicks=0),
            html.Button("Delete Power Change", id="delete-button", n_clicks=0),
            html.Div(id="segments-list"),
            dcc.Graph(id="power-graph"),
        ]
    )


time_segments = pd.DataFrame(columns=["Time", "Power"])

# validate input time military format
# identify current time, power
# start figure from current time to 24 hr from now
# show horizontal line at current power
# add new time, power: show power change at that time, add text will change and stay at power level
# add new time, power: show power cycling, add text, will change back and forth
# add propose (show viz) and confirm steps (send bos command)


@callback(
    [Output("segments-list", "children"), Output("power-graph", "figure")],
    [Input("add-button", "n_clicks"), Input("delete-button", "n_clicks")],
    [State("time", "value"), State("power-level", "value")],
    prevent_initial_call=True,
)
def update_segments_and_graph(add_clicks, delete_clicks, time, power):
    global time_segments
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    if "add-button" in changed_id and time and power:
        time = datetime.strptime(time, "%H%M").strftime("%H:%M")
        new_row = pd.DataFrame([[time, power]], columns=["Time", "Power"])
        time_segments = pd.concat([time_segments, new_row], ignore_index=True)
    elif "delete-button" in changed_id and time:
        time = datetime.strptime(time, "%H%M").strftime("%H:%M")
        time_segments = time_segments[time_segments["Time"] != time]

    time_segments["Time"] = pd.to_datetime(time_segments["Time"], format="%H:%M")
    time_segments.sort_values(by="Time", inplace=True)

    fig = go.Figure()

    print(f"{len(time_segments)} segments")

    for i, row in time_segments.iterrows():
        start_time = row["Time"]
        # Assuming next segment or end of day if last segment
        if i < len(time_segments) - 1:
            end_time = time_segments.iloc[i + 1]["Time"]
        else:
            # Extend to end of day if this is the last segment
            end_time = datetime.combine(datetime.today(), datetime.max.time())

        power_level = row["Power"]

        # Add a filled area to the figure
        fig.add_trace(
            go.Scatter(
                x=[start_time, end_time, end_time, start_time],
                y=[0, 0, power_level, power_level],
                fill="toself",
                mode="lines",
                name=f"Segment {i+1}",
            )
        )

    # Set the layout for the figure
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Power Level",
        xaxis=dict(tickmode="auto", nticks=24, tickformat="%H:%M"),
        yaxis=dict(range=[0, max(time_segments["Power"].astype(int)) + 100]),
    )  # Adjust y-axis range based on max power level

    return (
        html.Ul(
            children=[
                html.Li(f"{datetime.strftime(row['Time'], '%H:%M')}: {row['Power']}")
                for index, row in time_segments.iterrows()
            ]
        ),
        fig,
    )
