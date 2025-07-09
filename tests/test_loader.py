import pytest
from pathlib import Path
from src.loader import load_file


# проверка импорта и структуры
def test_load_file_structure():
    events = load_file(Path("data/test.json"))

    assert isinstance(events, list)
    assert len(events) > 0

    event = events[0]
    expected_keys = {"employee", "task", "start", "end", "type"}
    assert isinstance(event, dict)
    assert expected_keys.issubset(event.keys())
