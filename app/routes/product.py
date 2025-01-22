from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from ..routes.auth import get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/products", tags=["products"])
templates = Jinja2Templates(directory="app/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_products(request: Request, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@router.get("/{product_id}")
def read_product(product_id: int, request: Request, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("product.html", {"request": request, "product": product})