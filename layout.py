from dash import html, dcc


def create_layout(df):
    employees = sorted(df["employee"].unique())
    projects = sorted(df[df["type"] == "assignment"]["task"].unique())

    return html.Div([
        html.H1("Загруженность сотрудников", style={
            "textAlign": "center",
            "color": "#E0E0E0",
            "margin": "16px 0"
        }),

        html.Div([
            dcc.Dropdown(
                id="employee-filter",
                options=[{"label": emp, "value": emp} for emp in employees],
                multi=True,
                placeholder="Сотрудники",
                style={"width": "300px", "fontSize": "16px"}
            ),
            dcc.Dropdown(
                id="project-filter",
                options=[{"label": proj, "value": proj} for proj in projects],
                multi=True,
                placeholder="Проекты",
                style={"width": "300px", "fontSize": "16px"}
            ),
            dcc.Dropdown(
                id="scale-filter",
                options=[
                    {"label": "День", "value": "day"},
                    {"label": "Неделя", "value": "week"},
                    {"label": "Месяц", "value": "month"},
                ],
                value="day",
                placeholder="Масштаб времени",
                style={"width": "200px", "fontSize": "16px"}
            )
        ], style={
            "display": "flex",
            "gap": "16px",
            "padding": "0 20px",
            "marginBottom": "16px"
        }),
        dcc.Graph(id="gantt-graph", config={"displayModeBar": True}, style={
            "flexGrow": "1",
            "backgroundColor": "#121212"
        })
    ], style={
        "display": "flex",
        "flexDirection": "column",
        "height": "100vh",
        "backgroundColor": "#121212",
        "margin": "0",
        "padding": "0",
        "overflow": "hidden"
    })
