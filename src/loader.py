import json
import csv
from pathlib import Path


def load_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def load_csv(file_path):
    with open(file_path, "r") as f:
        data = list(csv.DictReader(f))
    return data


def load_file(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == ".json":
        return load_json(file_path)
    elif ext == ".csv":
        return load_csv(file_path)
    else:
        raise ValueError("Формат файла не поддерживается")
