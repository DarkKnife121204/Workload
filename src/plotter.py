import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import qualitative
from collections import defaultdict


# занятости
def get_overloads(df):
    overload = defaultdict(set)

    # создаем множество для занятости
    for index, row in df[df["type"] == "assignment"].iterrows():
        for day in pd.date_range(row["start"], row["end"]):
            overload[(row["employee"], day.date())].add(row["task"])

    # где более одной занятости
    overloaded_dates = {
        key for key, val in overload.items() if len(val) > 1
    }

    # отмечаем строки
    def is_overloaded(row):
        if row["type"] != "assignment":
            return False
        return any(
            (row["employee"], d.date()) in overloaded_dates
            for d in pd.date_range(row["start"], row["end"])
        )

    df["overloaded"] = df.apply(is_overloaded, axis=1)
    return df


def get_overlap(row, df):
    # ищем перекрытия
    overlaps = df[
        (df["employee"] == row["employee"]) &
        (df["task"] != row["task"]) &
        (df["type"] != "overtime") &
        (df["start"] < row["end"]) &
        (df["end"] > row["start"])
        ]["task"].tolist()

    return ", ".join(overlaps) if overlaps else "Нет перекрытий"


def get_color_map(df):
    # палитра цветов
    project_names = df.query("type == 'assignment'")["task"].unique()
    project_colors = qualitative.Pastel
    color_map = dict(zip(project_names, project_colors))
    color_map["Отпуск"] = "#A0A0A0"
    return color_map


def time_scale(scale, min_date, max_date):
    # диапазон от scale
    if scale == "day":
        tickformat = "%d %b"
        tick_interval = 24 * 60 * 60 * 1000
        range_padding = pd.Timedelta(days=2)
    elif scale == "week":
        tickformat = "%d %b"
        tick_interval = 7 * 24 * 60 * 60 * 1000
        range_padding = pd.Timedelta(days=7)
    elif scale == "month":
        tickformat = "%b %Y"
        tick_interval = "M1"
        range_padding = pd.Timedelta(days=15)
    else:
        tickformat = "%d %b"
        tick_interval = 24 * 60 * 60 * 1000
        range_padding = pd.Timedelta(days=2)

    return tickformat, tick_interval, [min_date - range_padding, max_date + range_padding]


def plot_gantt(events, scale):
    df = pd.DataFrame(events)

    # преобразуем время
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    df = get_overloads(df)

    # делим переработки
    df_timeline = df[df["type"] != "overtime"].copy()
    df_overtime = df[df["type"] == "overtime"]

    # перекрытия ищем
    df_timeline["overlaps"] = df_timeline.apply(lambda row: get_overlap(row, df_timeline), axis=1)

    # Цвета и обводка
    color_map = get_color_map(df_timeline)
    df_timeline["customdata"] = df_timeline[["overloaded"]].values

    # диаграмма
    fig = px.timeline(
        df_timeline,
        x_start="start",
        x_end="end",
        y="employee",
        color="task",
        text="task",
        color_discrete_map=color_map,
        opacity=0.8,
        custom_data=["overloaded"],
        hover_data={
            "employee": True,
            "task": True,
            "start": True,
            "end": True,
            "overlaps": True
        }
    )

    # Обводка при перегрузке
    for trace in fig.data:
        overloaded_mask = [cd[0] for cd in trace.customdata]
        line_colors = ["red" if ov else "rgba(0,0,0,0)" for ov in overloaded_mask]
        line_widths = [4 if ov else 0 for ov in overloaded_mask]
        trace.update(marker_line=dict(color=line_colors, width=line_widths))

    # переработки
    fig.add_trace(go.Scatter(
        x=df_overtime["start"],
        y=df_overtime["employee"],
        mode="markers+text",
        name="Переработка",
        marker=dict(
            symbol="diamond",
            size=12,
            color="#E45756",
            line=dict(width=1, color="black")
        ),
        hoverinfo="text+x+y",
        showlegend=True
    ))

    # масштабирование
    min_date = df["start"].min()
    max_date = df["end"].max()
    tickformat, tick_interval, x_range = time_scale(scale, min_date, max_date)

    # оформление диаграммы
    fig.update_layout(
        xaxis_title="Дата",
        yaxis_title="Сотрудник",
        font=dict(size=16, color="#E0E0E0"),
        legend_title="Тип занятости",
        legend=dict(font=dict(size=14)),
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#121212",
        xaxis=dict(
            tickformat=tickformat,
            dtick=tick_interval,
            range=x_range,
            gridcolor="#333333",
            zerolinecolor="#444444",
            linecolor="#555555",
            tickfont=dict(color="#E0E0E0")
        ),
        yaxis=dict(
            gridcolor="#333333",
            zerolinecolor="#444444",
            linecolor="#555555",
            tickfont=dict(color="#E0E0E0")
        )
    )

    # шрифт от scale
    if scale == "day":
        text_size = 18
    elif scale == "week":
        text_size = 14
    elif scale == "month":
        text_size = 10
    else:
        text_size = 12

    fig.update_traces(
        selector=dict(type="bar"),
        textfont=dict(size=text_size, color="white")
    )

    fig.update_yaxes(categoryorder='category ascending')

    return fig
