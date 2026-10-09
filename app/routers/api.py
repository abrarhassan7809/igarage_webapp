import re
from fastapi import APIRouter
from pydantic import BaseModel
from app import data

router = APIRouter(tags=["api"])
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

@router.get("/products")
def products(category: str = "All"):
    return data.filter_products(category)

@router.get("/iphones")
def product_details(series: str = "All", sort: str = "def"):
    return data.filter_iphones(series, sort)

@router.get("/stores")
def stores(city: str):
    q = city.strip().lower()
    n = data.STORES.get(q, 0)
    return {"city": q.title(), "count": n}

class Subscriber(BaseModel):
    email: str

@router.post("/subscribe")
def subscribe(body: Subscriber):
    if not EMAIL_RE.match(body.email):
        return {"ok": False, "message": "Enter a valid email address."}
    # TODO: persist to DB / mailing service
    return {"ok": True, "message": "Subscribed. Thanks!"}
