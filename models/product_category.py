from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class ProductCategory(SQLModel, table=True):
    __tablename__ = "product_category"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    
    # 建立与Product的反向关联
    products: List["Product"] = Relationship(back_populates="category")

    def __str__(self):
        return self.name