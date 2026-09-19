import math
from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select, func
from database import get_session
from models.news import News
from templating import templates

router = APIRouter(prefix="/news", tags=["新闻动态"])

@router.get("/list", response_class=HTMLResponse)
async def get_news_list(
    request: Request,
    session: Session = Depends(get_session),
    page: int = Query(1, gt=0)
):
    page_size = 10
    offset = (page - 1) * page_size
    
    # 查询数据（按时间倒序）
    stmt = select(News).order_by(News.created_at.desc()).offset(offset).limit(page_size)
    news_list = session.exec(stmt).all()
    
    # 计算总页数
    total_items = session.exec(select(func.count(News.id))).one()
    total_pages = math.ceil(total_items / page_size)
    
    return templates.TemplateResponse(request,"news/list.html", {
        "active_page": "news",
        "news_list": news_list,
        "total_pages": total_pages,
        "current_page": page
    })
    

from fastapi import HTTPException

@router.get("/detail/{news_id}", response_class=HTMLResponse)
async def get_news_detail(
    request: Request, 
    news_id: int, 
    session: Session = Depends(get_session)
):
    news_detail = session.get(News, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")
        
    return templates.TemplateResponse(request,"news/detail.html", {
        "active_page": "news",
        "news_detail": news_detail
    })