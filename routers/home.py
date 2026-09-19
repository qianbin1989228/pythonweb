from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from database import get_session
from templating import templates
from models.product import Product
from models.news import News

from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from fastapi import Response

def home_key_builder(func, namespace: str = "", request: Request = None, 
                     response: Response = None, *args, **kwargs):
    return "home_page_cache"

router = APIRouter(tags=["首页"])


# 在路由上添加缓存，设置有效期为60秒
@router.get("/", response_class=HTMLResponse)
@cache(expire=60, coder=PickleCoder, key_builder=home_key_builder)
async def read_root(request: Request, session: Session = Depends(get_session)):
    # 查询最新的4个产品与3条新闻
    products = session.exec(select(Product).order_by(Product.created_at.desc())
                   .limit(4)).all()
    news_list = session.exec(select(News).order_by(News.created_at.desc())
                    .limit(3)).all()
    
    context = {
        "active_page": "home",
        "products": products,
        "news_list": news_list
    }
    return templates.TemplateResponse(request,"home.html", context)