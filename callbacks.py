from dash.dependencies import Input, Output
from src.plotter import plot_gantt


def register_callbacks(app, df):
    @app.callback(
        Output("gantt-graph", "figure"),
        Input("employee-filter", "value"),
        Input("project-filter", "value"),
        Input("scale-filter", "value")
    )
    def update_figure(selected_employees, selected_projects, scale):
        filtered_data = df.copy()
        if selected_employees:
            filtered_data = filtered_data[filtered_data["employee"].isin(selected_employees)]
        if selected_projects:
            filtered_data = filtered_data[filtered_data["task"].isin(selected_projects)]
        return plot_gantt(filtered_data.to_dict("records"), scale=scale)
