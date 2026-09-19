from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .job_position import JobPosition

class ApplicationRecord(SQLModel, table=True):
    __tablename__ = "application_record"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    applicant_name: str = Field(description="应聘者姓名")
    applicant_email: str = Field(description="应聘者邮箱")
    applicant_phone: str = Field(description="应聘者电话")
    resume_path: str = Field(description="简历文件路径")
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    
    # 外键与关系定义
    job_position_id: Optional[int] = Field(default=None, foreign_key="job_position.id")
    job_position: Optional[JobPosition] = Relationship(back_populates="applications")