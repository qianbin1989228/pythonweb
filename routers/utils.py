import os, uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()
UPLOAD_DIR = "static/uploads"

@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="无效格式")
        
    # 生成UUID文件名防冲突
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as f:
        f.write(await file.read())
        
    # 返回TinyMCE要求的JSON格式
    return JSONResponse(content={"location": f"/{filepath.replace(os.path.sep, '/')}"})
    

UPLOAD_FILES_DIR = "static/uploads/files"

@router.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_FILES_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_FILES_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        
    location_url = f"/{file_path.replace(os.path.sep, '/')}"
    # 返回JSON，包含路径与原始文件名（用于生成链接文本）
    return JSONResponse(content={"location": location_url, "title": file.filename})
    
 
from fastapi.responses import FileResponse
from automation import EXCEL_FILE

from fastapi import Depends, Request
from auth_utils import get_current_superuser
from models.user import User

@router.get("/download/applications-report")
async def download_applications_report(
    request: Request, # 必须传入request供依赖项读取Session
    _user: User = Depends(get_current_superuser) # 触发鉴权逻辑
):
    if not os.path.exists(EXCEL_FILE):
        raise HTTPException(status_code=404, detail="报表文件不存在")
    return FileResponse(path=EXCEL_FILE, filename="applications.xlsx")