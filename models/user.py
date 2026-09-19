from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # 用户名，确保唯一性并建立索引优化查询
    username: str = Field(unique=True, index=True)
    # 仅存储哈希加密后的密码，绝不存储明文
    hashed_password: str
    # 权限标识，用于区分超级管理员
    is_superuser: bool = Field(default=False)