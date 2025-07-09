import json


# загрузка
def load_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return extract_events(data)


# структура из json
def extract_events(data):
    employee_map = {e["id"]: e["name"] for e in data["employees"]}
    project_map = {p["id"]: p["name"] for p in data["projects"]}

    events = []

    # назначения
    for a in data.get("assignments", []):
        events.append({
            "employee": employee_map[a["employee_id"]],
            "task": project_map[a["project_id"]],
            "start": a["start_date"],
            "end": a["end_date"],
            "type": "assignment"
        })

    # отпуска
    for v in data.get("vacations", []):
        events.append({
            "employee": employee_map[v["employee_id"]],
            "task": "Отпуск",
            "start": v["start_date"],
            "end": v["end_date"],
            "type": "vacation"
        })

    # переработки
    for o in data.get("overtimes", []):
        events.append({
            "employee": employee_map[o["employee_id"]],
            "task": "Переработка",
            "start": o["date"],
            "end": o["date"],
            "type": "overtime"
        })

    return events
