import json

# Функция загрузки данных из db.json
def load_db():
    try:
        with open("db.json", "r") as f:
            return json.load(f)  # Читаем JSON как список
    except FileNotFoundError:
        # Если файла нет, возвращаем пустой список
        return []

# Функция сохранения данных в db.json
def save_db(data):
    with open("db.json", "w") as f:
        json.dump(data, f)  # Записываем список в JSON

# Загружаем базу данных при старте
db = load_db()