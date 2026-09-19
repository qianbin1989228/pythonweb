from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlmodel import Session, select
from database import engine
from models.user import User
from auth_utils import verify_password, create_access_token, SECRET_KEY

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """处理SQLAdmin登录页面的提交"""
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        with Session(engine) as session:
            user = session.exec(select(User).where(User.username == username)).first()
            
            # 校验存在性、密码正确性及是否具有管理员权限
            if user and user.is_superuser and verify_password(password, 
                user.hashed_password):
                # 签发JWT并存入Session
                access_token = create_access_token(data={"sub": user.username})
                request.session.update({"token": f"bearer {access_token}"})
                return True
        return False

    async def logout(self, request: Request) -> bool:
        """登出并清空Session"""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """鉴权：检查Session中是否持有令牌"""
        token = request.session.get("token")
        if not token:
            return False
        return True

# 实例化认证后端
authentication_backend = AdminAuth(secret_key=SECRET_KEY)