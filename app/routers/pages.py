# pages.py
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from data import CATEGORIES, PRODUCTS, INDEX_PRODUCTS
from app.templating import templates
from db_config.database import get_db
from ..models.db_models.db_model import CategoryModel, ProductsModel
from pathlib import Path

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

router = APIRouter(tags=["templates"])

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request, "index.html",
        context={"STATIC_DIR": STATIC_DIR, "categories": CATEGORIES, "index_products": INDEX_PRODUCTS}
    )

@router.get("/products_page/")
def products_page(request: Request):
    return templates.TemplateResponse(
        request, "products_page.html",
        context={"STATIC_DIR": STATIC_DIR, "categories": CATEGORIES, "products": PRODUCTS}
    )

@router.get("/product_details/")
def product_details(request: Request, p_id: int):
    product = PRODUCTS.get(p_id) or PRODUCTS.get(str(p_id))

    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {p_id} not found")

    return templates.TemplateResponse(
        request, "product_details.html",
        context={"STATIC_DIR": STATIC_DIR, "product": product}
    )

@router.get("/accessories/")
def accessories(request: Request):
    return templates.TemplateResponse(request, "accessories_page.html", context={"STATIC_DIR": STATIC_DIR})

@router.get("/services/")
def services(request: Request):
    return templates.TemplateResponse(request, "services_page.html", context={"STATIC_DIR": STATIC_DIR})

@router.get("/exchange/")
def exchange(request: Request):
    return templates.TemplateResponse(request, "exchange_page.html", context={"STATIC_DIR": STATIC_DIR})