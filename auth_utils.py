from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """接收明文密码，返回bcrypt哈希值"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码与哈希密码是否匹配"""
    return pwd_context.verify(plain_password, hashed_password)
    

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt

# 用于签发JWT的密钥，生产环境需替换为长随机字符串
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    """生成包含用户信息的JWT令牌"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    

from fastapi import Depends, HTTPException, status, Request
from sqlmodel import Session, select
from database import get_session
from models.user import User

def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    """从Session中提取并验证JWT令牌，返回对应User对象"""
    token = request.session.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="用户未登录")
        
    token_pure = token.replace("bearer ", "")
    try:
        payload = jwt.decode(token_pure, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="令牌无效或已过期")
        
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user

def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """在登录的基础上，进一步校验是否为超级管理员"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="此操作需要超级管理员权限")
    return current_user
    
    
from datetime import date
from fastapi import Header
from models.api_user import ApiUser

def get_api_user_from_key(
    api_key: str = Header(None, alias="X-API-Key"),
    session: Session = Depends(get_session)
) -> ApiUser:
    if not api_key:
        raise HTTPException(status_code=401, detail="请求头中缺少 'X-API-Key'")

    api_user = session.exec(select(ApiUser).where(ApiUser.api_key == api_key)).first()
    if not api_user:
        raise HTTPException(status_code=401, detail="无效的API密钥")

    # 每日限额重置逻辑
    today = date.today()
    if api_user.last_api_call_date != today:
        api_user.last_api_call_date = today
        api_user.daily_api_calls_left = 10  # 每日限额10次

    # 检查余额
    if api_user.daily_api_calls_left <= 0:
        raise HTTPException(status_code=429, detail="今日API调用次数已达上限")

    # 扣减额度并持久化
    api_user.daily_api_calls_left -= 1
    api_user.api_call_count += 1
    session.add(api_user)
    session.commit()
    session.refresh(api_user)

    return api_user
    
    
def get_current_api_user_web(
    request: Request,
    session: Session = Depends(get_session)
) -> ApiUser:
    token = request.session.get("token")
    redirect_exp = HTTPException(
        status_code=307,
        headers={"Location": str(request.url_for('get_api_user_login'))}
    )
    if not token:
        raise redirect_exp

    try:
        payload = jwt.decode(token.replace("bearer ", ""), SECRET_KEY, 
                             algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise redirect_exp
    except JWTError:
        raise redirect_exp

    user = session.exec(select(ApiUser).where(ApiUser.username == username)).first()
    if not user:
        raise redirect_exp
    return user