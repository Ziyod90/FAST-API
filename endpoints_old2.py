from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from models import Item as ItemModel
from database_old import SessionLocal
from fastapi.templating import Jinja2Templates

# Dependency для БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def register_endpoints(app: FastAPI, templates: Jinja2Templates):
    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request, db: Session = Depends(get_db)):
        items = db.query(ItemModel).all()
        return templates.TemplateResponse("index.html", {"request": request, "items": items})

    @app.get("/add", response_class=HTMLResponse)
    async def add_item_form(request: Request):
        return templates.TemplateResponse("add_item.html", {"request": request})

    @app.post("/add")
    async def add_item(
        request: Request,
        name: str = Form(...),
        price: float = Form(...),
        description: str = Form(None),
        db: Session = Depends(get_db)
    ):
        if price > 100:
            raise HTTPException(status_code=400, detail="Too expensive")

        item = ItemModel(name=name, price=price, description=description)
        db.add(item)
        db.commit()
        db.refresh(item)
        return RedirectResponse("/", status_code=303)
