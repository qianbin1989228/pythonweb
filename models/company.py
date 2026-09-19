from typing import Optional
from sqlmodel import SQLModel, Field


class CompanyInfo(SQLModel, table=True):
    __tablename__ = "company_info"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 简介部分
    overview_title: str
    overview_image_url: str
    overview_lead_text: str
    
    # 发展历程部分
    history_1: str
    history_2: str
    history_3: str
    history_4: str
    
    # 企业文化部分
    culture_title: str
    culture_intro: str
    culture_item1_title: str
    culture_item1_text: str
    culture_item2_title: str
    culture_item2_text: str
    culture_item3_title: str
    culture_item3_text: str