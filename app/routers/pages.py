from fastapi import APIRouter, Request, HTTPException
from ..config import STATIC_DIR
from app.templating import templates

router = APIRouter()

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", context={"STATIC_DIR": STATIC_DIR})

@router.get("/iphones/")
def iphones(request: Request):
    return templates.TemplateResponse(request, "products_page.html")

@router.get("/product_details/")
def product_details(request: Request):
    return templates.TemplateResponse(request, "product_details.html")

@router.get("/accessories/")
def accessories(request: Request):
    return templates.TemplateResponse(request, "accessories_page.html")

@router.get("/services/")
def services(request: Request):
    return templates.TemplateResponse(request, "services_page.html")

@router.get("/exchange/")
def exchange(request: Request):
    return templates.TemplateResponse(request, "exchange_page.html")
