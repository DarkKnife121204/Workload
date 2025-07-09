import pytest
from src.plotter import plot_gantt
from pathlib import Path
from src.loader import load_file
import plotly.graph_objects as go


# проверка создание фигуры
def test_plot_gantt_returns_figure():
    events = load_file(Path("data/test.json"))
    fig = plot_gantt(events, "day")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
