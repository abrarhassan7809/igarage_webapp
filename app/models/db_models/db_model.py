# db_model.py
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db_config.database import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, default='')
    description = Column(String, default='')
    slug = Column(String, index=True, default='')

    # Relationship: One category has many products
    products = relationship("ProductsModel", back_populates="category", cascade="all, delete-orphan")


class ProductsModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default='')
    slug = Column(String, index=True, default='')
    brand = Column(String, default='Apple')
    description = Column(Text, default='')
    image_url = Column(String, default='')
    additional_images = Column(Text, default='')

    # Pricing & Stock
    original_price = Column(Float, default=0.0)
    discount_price = Column(Float, default=0.0)
    max_price = Column(Float, default=0.0)
    stock_quantity = Column(Integer, default=0)
    product_active = Column(Boolean, default=True)

    # Product Variant Attributes (Stored as comma-separated values, e.g., "Burgundy,Glacier,Silver")
    colors = Column(String, default='')
    storage_options = Column(String, default='')

    # Specifications
    display_spec = Column(String, default='')  # e.g., "6.9\" OLED, 120Hz"
    chip_spec = Column(String, default='')  # e.g., "A20 Pro"
    port_spec = Column(String, default='USB-C')
    water_resistance = Column(String, default='IP68')
    connectivity = Column(String, default='5G, Wi-Fi 7, Bluetooth')
    warranty = Column(String, default='2 Year (Apple + Mercantile) Warranty')
    pta_approved = Column(Boolean, default=True)
    benefits = Column(Text, default='')

    # Foreign Key linking to Categories
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Relationship back to Category
    category = relationship("CategoryModel", back_populates="products")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, default='')
    email = Column(String, unique=True, index=True, default='')
    hashed_password = Column(String, default='')
    phone_number = Column(String, default='')
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ServicesModel(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    repair_type = Column(String, default='')
    diagnostics = Column(String, default='')
    maintenance_package = Column(String, default='')
    pricing = Column(Float, default=0.0)
    estimated_turnaround_time = Column(String, default='')
    is_active = Column(Boolean, default=True)


class ExchangeModel(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    old_device_model = Column(String, default='')
    condition_details = Column(String, default='')
    uploaded_images = Column(String, default='')
    estimated_evaluation_value = Column(Float, default=0.0)
    status = Column(String, default='Pending')
    created_at = Column(DateTime, default=datetime.utcnow)

    # Optional relationship back to User
    user = relationship("UserModel", backref="exchanges")