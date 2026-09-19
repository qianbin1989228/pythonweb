from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class JobPosition(SQLModel, table=True):
    __tablename__ = "job_position"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, description="职位名称")
    department: str = Field(description="所属部门")
    content: str = Field(description="岗位职责")
    is_active: bool = Field(default=True, description="是否激活")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # 与应聘记录的关联
    applications: List["ApplicationRecord"] = Relationship(back_populates="job_position")

    def __str__(self):
        return self.title