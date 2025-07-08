from pathlib import Path
from src.loader import load_file, extract_events
from src.plotter import plot_gantt


if __name__ == "__main__":
    data = load_file(Path("data/test.json"))
    events = extract_events(data)
    plot_gantt(events, output_path=Path("output/gantt.html"))
