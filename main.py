from pathlib import Path
import webbrowser
import pandas as pd
from dash import Dash
from src.loader import load_file
from layout import create_layout
from callbacks import register_callbacks

# загрузка json
data = load_file(Path("data/test.json"))
df = pd.DataFrame(data)

# запуск dash
app = Dash(__name__)
app.index_string = open("layout.html", encoding="utf-8").read()
app.layout = create_layout(df)

# callback
register_callbacks(app, df)

# запуск
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050")
    app.run(debug=False)
