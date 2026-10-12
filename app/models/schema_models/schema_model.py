# schema_model.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# --- Category Schemas ---
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    slug: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    slug: str

    class Config:
        from_attributes = True


# --- Product Schemas ---
class ProductCreate(BaseModel):
    name: str
    slug: Optional[str] = None
    brand: Optional[str] = "Apple"
    description: Optional[str] = None
    image_url: Optional[str] = None
    additional_images: Optional[str] = None
    original_price: float = 0.0
    discount_price: float = 0.0
    max_price: Optional[float] = 0.0
    stock_quantity: int = 0
    product_active: bool = True

    # Specs & Options
    colors: Optional[str] = None
    storage_options: Optional[str] = None
    display_spec: Optional[str] = None
    chip_spec: Optional[str] = None
    port_spec: Optional[str] = "USB-C"
    water_resistance: Optional[str] = "IP68"
    connectivity: Optional[str] = "5G, Wi-Fi 7, Bluetooth"
    warranty: Optional[str] = "2 Year (Apple + Mercantile) Warranty"
    pta_approved: bool = True
    benefits: Optional[str] = None

    category_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    additional_images: Optional[str] = None
    original_price: Optional[float] = None
    discount_price: Optional[float] = None
    max_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    product_active: Optional[bool] = None

    colors: Optional[str] = None
    storage_options: Optional[str] = None
    display_spec: Optional[str] = None
    chip_spec: Optional[str] = None
    port_spec: Optional[str] = None
    water_resistance: Optional[str] = None
    connectivity: Optional[str] = None
    warranty: Optional[str] = None
    pta_approved: Optional[bool] = None
    benefits: Optional[str] = None

    category_id: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    slug: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    additional_images: Optional[str] = None
    original_price: float
    discount_price: float
    max_price: Optional[float] = None
    stock_quantity: int
    product_active: bool

    colors: Optional[str] = None
    storage_options: Optional[str] = None
    display_spec: Optional[str] = None
    chip_spec: Optional[str] = None
    port_spec: Optional[str] = None
    water_resistance: Optional[str] = None
    connectivity: Optional[str] = None
    warranty: Optional[str] = None
    pta_approved: bool
    benefits: Optional[str] = None

    category_id: Optional[int] = None
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True


# --- User / Admin Schemas ---
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    phone_number: Optional[str] = None
    is_admin: bool = False


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone_number: Optional[str] = None
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --- Service Schemas ---
class ServiceCreate(BaseModel):
    repair_type: str
    diagnostics: Optional[str] = None
    maintenance_package: Optional[str] = None
    pricing: float = 0.0
    estimated_turnaround_time: Optional[str] = None
    is_active: bool = True


class ServiceUpdate(BaseModel):
    repair_type: Optional[str] = None
    diagnostics: Optional[str] = None
    maintenance_package: Optional[str] = None
    pricing: Optional[float] = None
    estimated_turnaround_time: Optional[str] = None
    is_active: Optional[bool] = None


class ServiceResponse(BaseModel):
    id: int
    repair_type: str
    diagnostics: Optional[str] = None
    maintenance_package: Optional[str] = None
    pricing: float
    estimated_turnaround_time: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


# --- Exchange / Trade-In Schemas ---
class ExchangeCreate(BaseModel):
    old_device_model: str
    condition_details: Optional[str] = None
    uploaded_images: Optional[str] = None
    estimated_evaluation_value: float = 0.0


class ExchangeUpdate(BaseModel):
    old_device_model: Optional[str] = None
    condition_details: Optional[str] = None
    uploaded_images: Optional[str] = None
    estimated_evaluation_value: Optional[float] = None
    status: Optional[str] = None


class ExchangeResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    old_device_model: str
    condition_details: Optional[str] = None
    uploaded_images: Optional[str] = None
    estimated_evaluation_value: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True