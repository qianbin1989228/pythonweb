import math
from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select, func, or_
from database import get_session
from models.product import Product
from models.product_category import ProductCategory
from templating import templates

router = APIRouter(prefix="/products", tags=["产品中心"])

@router.get("/list", response_class=HTMLResponse)
async def get_product_list(
    request: Request,
    session: Session = Depends(get_session),
    page: int = Query(1, gt=0),
    category_id: int = Query(None),
    q: str = Query(None)
):
    page_size = 9
    
    # 1. 获取所有类别供侧边栏渲染
    categories = session.exec(select(ProductCategory)).all()
    
    # 2. 构建动态查询条件
    query = select(Product)
    if category_id:
        query = query.where(Product.category_id == category_id)
    if q:
        # 使用or_实现名称与内容的模糊搜索
        query = query.where(or_(Product.name.contains(q), Product.content.contains(q)))
        
    # 3. 计算分页总数
    total_query = select(func.count()).select_from(query.alias())
    total_items = session.exec(total_query).one()
    total_pages = math.ceil(total_items / page_size)
    
    # 4. 获取当前页数据
    product_list = session.exec(
        query.order_by(Product.created_at.desc())
        .offset((page - 1) * page_size).limit(page_size)
    ).all()
    
    context = {
        "active_page": "products",
        "product_list": product_list, "categories": categories,
        "total_pages": total_pages, "current_page": page,
        "current_category_id": category_id, "search_query": q
    }
    return templates.TemplateResponse(request,"product/list.html", context)
    
    
from fastapi import HTTPException

@router.get("/detail/{product_id}", response_class=HTMLResponse)
async def get_product_detail(
    request: Request, 
    product_id: int, 
    session: Session = Depends(get_session)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return templates.TemplateResponse(request,"product/detail.html", {
        "active_page": "products", "product": product
    })