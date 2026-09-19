from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .product_category import ProductCategory

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # 物理层面的外键约束
    category_id: Optional[int] = Field(default=None, foreign_key="product_category.id")
    # ORM层面的关系绑定
    category: Optional[ProductCategory] = Relationship(back_populates="products")