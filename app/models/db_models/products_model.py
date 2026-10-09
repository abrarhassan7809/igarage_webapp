from sqlalchemy import Column, Integer, String
from db_config.database import Base


class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    image_url = Column(String)
    price = Column(String)

