# api.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from db_config.database import get_db
from ..models.db_models.db_model import (
    ProductsModel, CategoryModel, ServicesModel, ExchangeModel
)
from ..models.schema_models.schema_model import (
    ProductCreate, ProductUpdate,
    CategoryCreate, CategoryUpdate, CategoryResponse,
    ServiceCreate, ServiceUpdate, ServiceResponse,
    ExchangeCreate, ExchangeUpdate, ExchangeResponse
)
from typing import List, Optional
import shutil
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

router = APIRouter(tags=["api"])

# ==================== PRODUCT ENDPOINTS ====================

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductsModel).all()

@router.get("/product_details/{product_id}")
def product_details(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductsModel).filter(ProductsModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 1. ADD PRODUCT (Create)
@router.post("/add/", status_code=status.HTTP_201_CREATED)
def add_product(
        name: str = Form(...),
        slug: Optional[str] = Form(None),
        brand: Optional[str] = Form("Apple"),
        description: Optional[str] = Form(None),
        original_price: float = Form(0.0),
        discount_price: float = Form(0.0),
        max_price: Optional[float] = Form(0.0),
        stock_quantity: int = Form(0),
        product_active: bool = Form(True),
        colors: Optional[str] = Form(None),
        storage_options: Optional[str] = Form(None),
        display_spec: Optional[str] = Form(None),
        chip_spec: Optional[str] = Form(None),
        port_spec: Optional[str] = Form("USB-C"),
        water_resistance: Optional[str] = Form("IP68"),
        connectivity: Optional[str] = Form("5G, Wi-Fi 7, Bluetooth"),
        warranty: Optional[str] = Form("2 Year (Apple + Mercantile) Warranty"),
        pta_approved: bool = Form(True),
        benefits: Optional[str] = Form(None),
        category_id: Optional[int] = Form(None),
        image_url: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db)):

    final_image_url = image_url

    if file and file.filename:
        upload_folder = os.path.join(STATIC_DIR, "web_img")
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        final_image_url = f"\\static\\web_img\\{file.filename}"

    elif final_image_url:
        if not final_image_url.startswith("\\static\\web_img\\") and not final_image_url.startswith("/static/web_img/"):
            image_url_cleaned = final_image_url.lstrip("\\/")
            final_image_url = f"\\static\\web_img\\{image_url_cleaned}"

    new_product = ProductsModel(
        name=name,
        slug=slug,
        brand=brand,
        description=description,
        image_url=final_image_url,
        original_price=original_price,
        discount_price=discount_price,
        max_price=max_price,
        stock_quantity=stock_quantity,
        product_active=product_active,
        colors=colors,
        storage_options=storage_options,
        display_spec=display_spec,
        chip_spec=chip_spec,
        port_spec=port_spec,
        water_resistance=water_resistance,
        connectivity=connectivity,
        warranty=warranty,
        pta_approved=pta_approved,
        benefits=benefits,
        category_id=category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product added successfully", "product": new_product}


# 2. PARTIAL UPDATE PRODUCT (PATCH)
@router.patch("/update/{product_id}")
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(ProductsModel).filter(ProductsModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return {"message": "Product updated successfully", "product": product}


# 3. ACTIVATE / DEACTIVATE PRODUCT
@router.patch("/status/{product_id}")
def toggle_product_status(product_id: int, active_status: bool, db: Session = Depends(get_db)):
    product = db.query(ProductsModel).filter(ProductsModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.product_active = active_status
    db.commit()
    db.refresh(product)

    status_word = "activated" if active_status else "deactivated"
    return {"message": f"Product successfully {status_word}", "product_active": product.product_active}


# 4. DELETE PRODUCT
@router.delete("/delete/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductsModel).filter(ProductsModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}


# ==================== CATEGORY ENDPOINTS ====================

@router.post("/categories/add/", status_code=status.HTTP_201_CREATED)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(CategoryModel).filter(CategoryModel.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = CategoryModel(
        name=category.name,
        description=category.description,
        slug=category.slug
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"message": "Category added successfully", "category": new_category}

@router.patch("/categories/update/{category_id}")
def update_category(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = category_data.dict(exclude_unset=True)

    if "name" in update_data:
        existing = db.query(CategoryModel).filter(
            CategoryModel.name == update_data["name"],
            CategoryModel.id != category_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Category name already exists")

    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return {"message": "Category updated successfully", "category": category}

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(CategoryModel).all()

@router.delete("/categories/delete/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}


# ==================== SERVICE ENDPOINTS ====================

@router.post("/services/add/", status_code=status.HTTP_201_CREATED)
def add_service(service: ServiceCreate, db: Session = Depends(get_db)):
    new_service = ServicesModel(**service.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return {"message": "Service added successfully", "service": new_service}

@router.get("/services", response_model=List[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(ServicesModel).all()

@router.patch("/services/update/{service_id}")
def update_service(service_id: int, service_data: ServiceUpdate, db: Session = Depends(get_db)):
    service = db.query(ServicesModel).filter(ServicesModel.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    update_data = service_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(service, key, value)

    db.commit()
    db.refresh(service)
    return {"message": "Service updated successfully", "service": service}

@router.delete("/services/delete/{service_id}", status_code=status.HTTP_200_OK)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(ServicesModel).filter(ServicesModel.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()
    return {"message": "Service deleted successfully"}


# ==================== EXCHANGE / TRADE-IN ENDPOINTS ====================
@router.post("/exchange/add/", status_code=status.HTTP_201_CREATED)
def add_exchange(exchange: ExchangeCreate, db: Session = Depends(get_db)):
    new_exchange = ExchangeModel(**exchange.dict())
    db.add(new_exchange)
    db.commit()
    db.refresh(new_exchange)
    return {"message": "Exchange request submitted successfully", "exchange": new_exchange}

@router.get("/exchange/requests", response_model=List[ExchangeResponse])
def get_exchange_requests(db: Session = Depends(get_db)):
    return db.query(ExchangeModel).all()

@router.patch("/exchange/update/{exchange_id}")
def update_exchange(exchange_id: int, exchange_data: ExchangeUpdate, db: Session = Depends(get_db)):
    exchange = db.query(ExchangeModel).filter(ExchangeModel.id == exchange_id).first()
    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange request not found")

    update_data = exchange_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(exchange, key, value)

    db.commit()
    db.refresh(exchange)
    return {"message": "Exchange request updated successfully", "exchange": exchange}

@router.delete("/exchange/delete/{exchange_id}", status_code=status.HTTP_200_OK)
def delete_exchange(exchange_id: int, db: Session = Depends(get_db)):
    exchange = db.query(ExchangeModel).filter(ExchangeModel.id == exchange_id).first()
    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange request not found")

    db.delete(exchange)
    db.commit()
    return {"message": "Exchange request deleted successfully"}