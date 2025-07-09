import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import qualitative


# условия перекрытий
def get_overlaps(row, df):
    overlaps = df[
        (df["employee"] == row["employee"]) &
        (df["task"] != row["task"]) &
        (df["type"] != "overtime") &
        (df["start"] < row["end"]) &
        (df["end"] > row["start"])
        ]["task"].tolist()
    return ", ".join(overlaps) if overlaps else "Нет перекрытий"


def plot_gantt(events, output_path):
    df = pd.DataFrame(events)

    # время
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])

    # разделение
    df_timeline = df[df["type"] != "overtime"].copy()
    df_overtime = df[df["type"] == "overtime"]

    # вычисление перекрытий
    df_timeline["overlaps"] = df_timeline.apply(lambda row: get_overlaps(row, df_timeline), axis=1)

    # цвета
    project_names = df_timeline.query("type == 'assignment'")["task"].unique()
    project_colors = qualitative.Pastel
    color_map = dict(zip(project_names, project_colors))
    color_map["Отпуск"] = "#A0A0A0"

    # основной график
    fig = px.timeline(
        df_timeline,
        x_start="start",
        x_end="end",
        y="employee",
        color="task",
        text="task",
        color_discrete_map=color_map,
        opacity=0.6,
        hover_data={
            "employee": True,
            "task": True,
            "start": True,
            "end": True,
            "overlaps": True
        }
    )

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

    # оформление
    fig.update_layout(
        title="Загруженность сотрудников",
        title_font_size=24,
        xaxis_title="Дата",
        yaxis_title="Сотрудник",
        font=dict(size=16, color="#E0E0E0"),
        legend_title="Тип занятости",
        legend=dict(font=dict(size=14)),
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#121212",
        xaxis=dict(
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

    fig.update_traces(
        selector=dict(type="bar"),
        textfont=dict(size=18, color="white")
    )

    fig.update_yaxes(categoryorder='category ascending')

    fig.write_html(output_path)
    print(f"Диаграмма сохранена: {output_path}")
