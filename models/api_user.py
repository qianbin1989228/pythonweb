from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class ApiUser(SQLModel, table=True):
    __tablename__ = "api_user"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    
    # 用于程序化调用的凭证，保持唯一并添加索引
    api_key: str = Field(unique=True, index=True)
    
    # 速率限制相关字段
    api_call_count: int = Field(default=0)
    last_api_call_date: Optional[date] = Field(default=None)
    daily_api_calls_left: int = Field(default=10)