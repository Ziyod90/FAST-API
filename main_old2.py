from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from endpoints_old2 import register_endpoints
from database_old import Base, engine

# Создаём таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключаем шаблоны и статику
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Регистрируем эндпойнты
register_endpoints(app, templates)
