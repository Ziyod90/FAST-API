from fastapi import FastAPI
from endpoints import register_endpoints

# Создаём приложение FastAPI
app = FastAPI(
    title="My FastAPI Example",
    description="Пример API с GET и POST запросами",
    version="1.0.0",
)

# Регистрируем эндпойнты
register_endpoints(app)
