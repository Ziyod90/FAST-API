from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from pydantic import BaseModel
from enum import Enum
from auth import get_key, get_user, admin_only
from database import db, save_db
from typing import Annotated
import shutil
from pathlib import Path


class Model(str, Enum):
    a = "a"
    b = "b"


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class Item(BaseModel):
    name: str
    price: float
    description: str | None = None


def register_endpoints(app: FastAPI):
    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/items/{item_id}")
    async def read_item(item_id: int, q: str = None, key=Depends(get_key)):
        return {"item_id": item_id, "q": q}

    @app.get("/models/{model}")
    async def get_model(model: Model):
        return {"model": model}

    @app.get("/users/me")
    async def read_user_me(user: str = Depends(get_user)):  # Эндпойнт с HTTP Basic
        return {"user_id": user}

    @app.get("/users/{user_id}")
    async def read_user(user_id: str):
        return {"user_id": user_id}

    @app.post("/items/")
    async def create_item(item: Item):
        # Проверяем цену
        if item.price > 100:
            raise HTTPException(status_code=400, detail="Too expensive")
        db.append(item.dict())  # Добавляем товар в список
        save_db(db)  # Сохраняем в db.json
        return item

    # Эндпойнт только для админа
    @app.get("/admin/")
    async def admin_only_endpoint(user: str = Depends(admin_only)):
        return {"message": "Welcome, admin"}

    # Эндпойнт для получения всех товаров
    @app.get("/items/")
    async def get_items():
        return db

    @app.post("/uploadfile/")
    async def create_upload_file(file: UploadFile = File(...)):
        file_path = UPLOAD_DIR / file.filename

        # Сохраняем на диск
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"filename": file.filename, "saved_to": str(file_path)}
