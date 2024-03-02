import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_status_fig(df: pd.DataFrame) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df["datetime"], y=df["hashrate"], name="Hashrate"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df["datetime"], y=df["temperature_avg"], name="Temperature"),
        secondary_y=True,
    )

    fig.update_layout(
        title="Hashrate and Temperature over Time",
        xaxis_title="Time",
    )
    fig.update_yaxes(title_text="Hashrate", secondary_y=False)
    fig.update_yaxes(title_text="Temperature", secondary_y=True)
    fig.update_yaxes(range=[0, 50], secondary_y=False)
    fig.update_yaxes(range=[0, 100], secondary_y=True)
    return fig


def get_hashrate_fig(df: pd.DataFrame) -> go.Figure:
    avg_hashrate = (
        df[["hashboard_0_hashrate", "hashboard_1_hashrate", "hashboard_2_hashrate"]]
        .mean(axis=0)
        .sum()
    )

    fig = px.line(
        df,
        x="datetime",
        y=["hashboard_0_hashrate", "hashboard_1_hashrate", "hashboard_2_hashrate"],
        labels={"value": "Hashrate", "variable": "Hashboard"},
        title="Hashrate over Time",
    )

    for trace, new_name in zip(fig.data, ["0", "1", "2"]):
        trace.name = new_name

    fig.add_hline(
        y=avg_hashrate,
        line_dash="dot",
        annotation_text=f"Average Hashrate ({avg_hashrate.round(2)} TH/s)",
        annotation_position="bottom right",
    )
    fig.update_yaxes(range=[0, avg_hashrate * 1.1])

    return fig


def get_temperature_fig(df: pd.DataFrame) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    temp_cols = [col for col in df.columns if "hashboard_" in col and "temp" in col]
    for col in temp_cols:
        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df[col],
                name=col.replace("hashboard_", "")
                .replace("_chip_temp", " Chip")
                .replace("_temp", " Board"),
            ),
            secondary_y=False,
        )

    fan_cols = [
        col for col in df.columns if col.startswith("fan_") and col.endswith("_speed")
    ]
    for col in fan_cols:
        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df[col],
                name=col.replace("fan_", "Fan ").replace("_speed", ""),
                line=dict(dash="dot"),
            ),
            secondary_y=True,
        )

    fig.update_layout(title="Temperature and Fan Speed over Time", xaxis_title="Time")
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
    fig.update_yaxes(title_text="Speed (RPM)", secondary_y=True)

    fig.update_yaxes(range=[0, 115], secondary_y=False)
    fig.update_yaxes(range=[0, 8000], secondary_y=True)

    fig.add_hline(
        y=110,
        line_color="red",
        annotation_text="Dangerous (110 °C)",
        annotation_position="bottom left",
        secondary_y=False,
    )
    fig.add_hline(
        y=100,
        line_color="orange",
        annotation_text="Hot (100 °C)",
        annotation_position="bottom left",
        secondary_y=False,
    )
    return fig
