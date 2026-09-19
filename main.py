from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqladmin import Admin
from database import engine
from admin import CompanyInfoAdmin, NewsAdmin, ProductCategoryAdmin, ProductAdmin,JobPositionAdmin,ApplicationRecordAdmin
from admin import ApiUserAdmin
from routers import company,utils,news,product,recruitment,support,home
from templating import templates

from starlette.middleware.sessions import SessionMiddleware
from auth_utils import SECRET_KEY
from admin_auth import authentication_backend

# 初始化应用并禁用默认在线文档URL
app = FastAPI(
    title="派森科技",
    description="Python Web开发从入门到实战",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

# 注册Session中间件，必须提供secret_key
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# 绑定Admin并注册视图
admin = Admin(
    app, 
    engine, 
    title="派森科技后台管理系统",
    authentication_backend=authentication_backend
)

admin.add_view(CompanyInfoAdmin)
admin.add_view(NewsAdmin)
admin.add_view(ProductCategoryAdmin)
admin.add_view(ProductAdmin)
admin.add_view(JobPositionAdmin)
admin.add_view(ApplicationRecordAdmin)
admin.add_view(ApiUserAdmin)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置离线API文档路由
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - API Docs",
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
    )

# 注册业务模块路由
app.include_router(company.router)
app.include_router(utils.router)
app.include_router(news.router)
app.include_router(product.router)
app.include_router(recruitment.router)
app.include_router(support.router)
app.include_router(home.router)
    
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")