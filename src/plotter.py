import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import qualitative


def plot_gantt(events, output_path):
    df = pd.DataFrame(events)

    # время
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])

    # разделение
    df_timeline = df[df["type"] != "overtime"]
    df_overtime = df[df["type"] == "overtime"]

    # цвета
    project_names = df_timeline.query("type == 'assignment'")["task"].unique()
    project_colors = qualitative.Pastel
    color_map = dict(zip(project_names, project_colors))
    color_map["Отпуск"] = "#A0A0A0"

    # основной
    fig = px.timeline(
        df_timeline,
        x_start="start",
        x_end="end",
        y="employee",
        color="task",
        text="task",
        color_discrete_map=color_map
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
        text="Переработка",
        textposition="top center",
        hoverinfo="text+x+y",
        showlegend=True
    ))

    # оформление
    fig.update_layout(
        title="Загруженность сотрудников",
        xaxis_title="Дата",
        yaxis_title="Сотрудник",
        font=dict(size=14),
        margin=dict(l=100, r=20, t=50, b=60),
        legend_title="Тип занятости"
    )

    fig.update_yaxes(categoryorder='category ascending')

    fig.write_html(output_path)
    print(f"Диаграмма сохранена: {output_path}")
