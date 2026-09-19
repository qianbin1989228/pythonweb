from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from templating import templates

router = APIRouter(prefix="/support", tags=["服务支持"])

@router.get("/register", response_class=HTMLResponse)
async def get_api_user_register_page(request: Request, error: str = None):
    return templates.TemplateResponse(
        request,"support/register.html", 
        {"error_message": error}
    )
    

import secrets
from fastapi import Depends, Form
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from database import get_session
from models.api_user import ApiUser
from auth_utils import hash_password

@router.post("/register", response_class=HTMLResponse)
async def handle_api_user_register(
    request: Request,
    session: Session = Depends(get_session),
    username: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...)
):
    # 1. 校验密码一致性
    if password != password_confirm:
        return templates.TemplateResponse(request,"support/register.html", {
            "error_message": "两次输入的密码不一致，请重新输入。"
        })

    # 2. 校验用户名唯一性
    existing_user = session.exec(
                        select(ApiUser).where(ApiUser.username == username)).first()
    if existing_user:
        return templates.TemplateResponse(request,"support/register.html", {
            "error_message": f"用户名 '{username}' 已被注册。"
        })

    # 3. 创建新用户及API密钥
    new_api_user = ApiUser(
        username=username,
        hashed_password=hash_password(password),
        api_key=secrets.token_hex(16)
    )
    session.add(new_api_user)
    session.commit()

    # 4. 注册成功后重定向至登录页（带成功标识）
    login_url = request.url_for('get_api_user_login')
    return RedirectResponse(url=f"{login_url}?registered=true", status_code=303)
    
    
@router.get("/tools", response_class=HTMLResponse)
async def get_online_tools(request: Request):
    return templates.TemplateResponse(request,"support/tools.html", {
        "active_page": "support"
    })
    

from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from services.qrcode_service import generate_qrcode_image, decode_qrcode_from_image

@router.post("/tools/generate")
async def handle_online_generate(text: str = Form(...)):
    img_buffer = generate_qrcode_image(text)
    return StreamingResponse(img_buffer, media_type="image/png")

@router.post("/tools/decode")
async def handle_online_decode(file: UploadFile = File(...)):
    results = await decode_qrcode_from_image(file)
    return JSONResponse(content=results)
    
    
from pydantic import BaseModel
from auth_utils import get_api_user_from_key

class QRCodeRequest(BaseModel):
    text: str

@router.post("/api/v1/qrcode/generate")
async def api_generate_qrcode(
    request_data: QRCodeRequest,
    api_user: ApiUser = Depends(get_api_user_from_key)
):
    img_buffer = generate_qrcode_image(request_data.text)
    return StreamingResponse(img_buffer, media_type="image/png")

@router.post("/api/v1/qrcode/decode")
async def api_decode_qrcode(
    file: UploadFile = File(...),
    api_user: ApiUser = Depends(get_api_user_from_key)
):
    results = await decode_qrcode_from_image(file)
    return JSONResponse(content=results)
    

from auth_utils import verify_password, create_access_token

@router.get("/login", response_class=HTMLResponse)
async def get_api_user_login(request: Request, registered: bool = False):
    return templates.TemplateResponse(request,"support/login.html", {
        "show_success_message": registered
    })

@router.post("/login")
async def handle_api_user_login(
    request: Request,
    session: Session = Depends(get_session),
    username: str = Form(...),
    password: str = Form(...)
):
    request.session.clear()
    user = session.exec(select(ApiUser).where(ApiUser.username == username)).first()
    
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(request,"support/login.html", {
            "error_message": "用户名或密码不正确。"
        })

    access_token = create_access_token(data={"sub": user.username})
    request.session.update({"token": f"bearer {access_token}"})
    
    return RedirectResponse(url=request.url_for('get_user_dashboard_page'), 
                            status_code=303)

@router.get("/logout")
async def handle_api_user_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=request.url_for('get_api_user_login'), 
                            status_code=303)
                            
                            
from auth_utils import get_current_api_user_web

@router.get("/dashboard", response_class=HTMLResponse)
async def get_user_dashboard_page(
    request: Request,
    current_user: ApiUser = Depends(get_current_api_user_web)
):
    return templates.TemplateResponse(request,"support/dashboard.html", {
        "active_page": "support", "user": current_user
    })
    


import httpx
from pydantic import BaseModel
from services.llm_service import build_company_knowledge_base

class ChatRequest(BaseModel):
    message: str

LLM_API_KEY = "sk-xxxxxxxxxx" # 替换为自己的平台密钥API_KEY
LLM_API_URL = "https://api.siliconflow.cn/v1/chat/completions" # 例如采用硅基流动平台


MODEL_NAME = "Qwen/Qwen3-8B"

@router.post("/api/chat")
async def chat_with_ai(chat_req: ChatRequest):
    system_prompt = build_company_knowledge_base()
    payload = {
        "model": MODEL_NAME,
        "messages":[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chat_req.message}
        ],
        "temperature": 0.7
    }
    headers = {"Authorization": f"Bearer {LLM_API_KEY}"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(LLM_API_URL, json=payload, 
                                         headers=headers, timeout=30.0)
            response.raise_for_status()
            ai_reply = response.json()["choices"][0]["message"]["content"]
            return {"reply": ai_reply}
        except Exception:
            return {"reply": "抱歉，智能客服暂时繁忙，请稍后再试。"}