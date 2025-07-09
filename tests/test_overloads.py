import pytest
import pandas as pd
from src.plotter import get_overloads, get_overlap


@pytest.fixture
def test_df():
    return pd.DataFrame([
        {
            "employee": "Иванов",
            "task": "Проект A",
            "start": "2025-07-01",
            "end": "2025-07-03",
            "type": "assignment"
        },
        {
            "employee": "Иванов",
            "task": "Проект B",
            "start": "2025-07-02",
            "end": "2025-07-04",
            "type": "assignment"
        },
        {
            "employee": "Иванов",
            "task": "Отпуск",
            "start": "2025-07-10",
            "end": "2025-07-15",
            "type": "vacation"
        }
    ])


def test_mark_overloads_adds_column(test_df):
    df = test_df.copy()
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])

    result = get_overloads(df)

    assert "overloaded" in result.columns
    assert result.loc[0, "overloaded"] == True
    assert result.loc[1, "overloaded"] == True
    assert result.loc[2, "overloaded"] == False


def test_get_overlaps_returns_correct_tasks(test_df):
    df = test_df.copy()
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])

    row = df.iloc[0]
    overlaps = get_overlap(row, df)

    assert "Проект B" in overlaps
    assert "Проект A" not in overlaps
    assert "Отпуск" not in overlaps
