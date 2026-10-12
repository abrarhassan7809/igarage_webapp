# pages.py
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from ..config import STATIC_DIR
from app.templating import templates
from db_config.database import get_db
from ..models.db_models.db_model import CategoryModel, ProductsModel

router = APIRouter(tags=["templates"])

@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    categories = db.query(CategoryModel).all()
    products = db.query(ProductsModel).all()
    return templates.TemplateResponse(
        request, "index.html", context={
            "STATIC_DIR": STATIC_DIR, "categories": categories, "products": products
        }
    )

@router.get("/products_page/")
def products_page(request: Request):
    return templates.TemplateResponse(request, "products_page.html", context={"STATIC_DIR": STATIC_DIR})


@router.get("/product_details/")
def product_details(request: Request, p_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductsModel).filter(ProductsModel.id == p_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return templates.TemplateResponse(
        request, "product_details.html", context={"STATIC_DIR": STATIC_DIR, "product": product}
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