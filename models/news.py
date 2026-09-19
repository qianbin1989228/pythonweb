from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class News(SQLModel, table=True):
    __tablename__ = "news"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str  # 存储富文本编辑器生成的 HTML
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)