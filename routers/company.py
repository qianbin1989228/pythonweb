from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from sqlmodel import Session, select
from database import get_session
from models.company import CompanyInfo

router = APIRouter(prefix="/company", tags=["公司简介"])
templates = Jinja2Templates(directory="templates")

@router.get("/about", response_class=HTMLResponse)
async def get_company_about_page(
    request: Request,
    session: Session = Depends(get_session)
):
    # 查询数据库中的第一条公司信息
    statement = select(CompanyInfo)
    company_info = session.exec(statement).first()
    
    context = {
        "active_page": "company",
        "company_info": company_info 
    }
    return templates.TemplateResponse(request,"company/about.html", context)