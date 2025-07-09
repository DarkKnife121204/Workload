# Workload

Система визуализации загруженности сотрудников

## Возможности

- Импорт данных из JSON 
- Визуализация в виде диаграммы Ганта (Plotly)
- Фильтрация по проектам и сотрудникам
- Подсветка перегрузок
- Поддержка событий:
    - Назначения
    - Отпуск
    - Переработка
- Интерактивный веб-интерфейс (Dash)

## Установка и использование
```bash
git clone https://github.com/DarkKnife121204/Workload
cd Workload
pip install -r requirements.txt
python main.py
```
Экспортируется JSON файл из data.

Пример формата входных данных:
```json
{
  "employees": [
    {"id": 1, "name": "Иванов И.И."},
    {"id": 2, "name": "Петров П.П."}
  ],
  "projects": [
    {"id": 10, "name": "Проект А"},
    {"id": 11, "name": "Проект Б"},
    {"id": 12, "name": "Проект В"}
  ],
  "assignments": [
    {"employee_id": 1, "project_id": 10, "start_date": "2025-06-01", "end_date": "2025-06-15"},
    {"employee_id": 1, "project_id": 11, "start_date": "2025-06-16", "end_date": "2025-06-30"},
    {"employee_id": 2, "project_id": 11, "start_date": "2025-06-01", "end_date": "2025-06-30"}
  ],
  "vacations": [
    {"employee_id": 1, "start_date": "2025-06-10", "end_date": "2025-06-12"}
  ],
  "overtimes": [
    {"employee_id": 1, "date": "2025-06-08"},
    {"employee_id": 2, "date": "2025-06-15"}
  ]
}
```

## Тестирование

Для запуска тестов выполните команду:

```bash
pytest tests/
```
## Стек 

- **Язык программирования:** Python 
- **Визуализация:** Plotly, Dash
- **Обработка данных:** pandas
- **Форматы входных данных:** JSON
- **Тестирование:** pytest
