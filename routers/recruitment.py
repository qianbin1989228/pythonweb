from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from database import get_session
from models.job_position import JobPosition
from templating import templates

from fastapi import BackgroundTasks
from automation import write_application_to_excel

router = APIRouter(prefix="/recruitment", tags=["人才招聘"])

@router.get("/jobs", response_class=HTMLResponse)
async def get_job_list(request: Request, session: Session = Depends(get_session)):
    # 仅查询已激活的岗位，按时间倒序
    statement = select(JobPosition).where(JobPosition.is_active == 
                    True).order_by(JobPosition.created_at.desc())
    job_list = session.exec(statement).all()
    
    return templates.TemplateResponse(request,"recruitment/list.html", {
        "active_page": "recruitment", "job_list": job_list
    })

@router.get("/job/{job_id}", response_class=HTMLResponse)
async def get_job_detail(request: Request, job_id: int, 
                              session: Session = Depends(get_session)):
    job_detail = session.get(JobPosition, job_id)
    if not job_detail or not job_detail.is_active:
        raise HTTPException(status_code=404, detail="岗位不存在或已失效")
        
    return templates.TemplateResponse(request,"recruitment/detail.html", {
        "active_page": "recruitment", "job_detail": job_detail
    })


@router.get("/apply/success", response_class=HTMLResponse)
async def get_success_page(request: Request):
    return templates.TemplateResponse(request,"recruitment/success.html", {
        "active_page": "recruitment"
    })


@router.get("/apply/{job_id}", response_class=HTMLResponse)
async def get_application_form(request: Request, job_id: int, 
                               session: Session = Depends(get_session)):
    job_position = session.get(JobPosition, job_id)
    if not job_position or not job_position.is_active:
        raise HTTPException(status_code=404, detail="岗位不存在或已失效")
        
    return templates.TemplateResponse(request,"recruitment/apply.html", {
        "active_page": "recruitment", "job_position": job_position
    })
    
    
import os
import uuid
from fastapi import Form, UploadFile, File
from fastapi.responses import RedirectResponse
from models.application_record import ApplicationRecord

RESUME_DIR = "static/resumes"

@router.post("/apply/{job_id}")
async def handle_application_form(
    request: Request, job_id: int, 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    applicant_name: str = Form(...),
    applicant_email: str = Form(...),
    applicant_phone: str = Form(...),
    resume: UploadFile = File(...),
):
    # 验证岗位有效性
    job_position = session.get(JobPosition, job_id)
    if not job_position or not job_position.is_active:
        raise HTTPException(status_code=404, detail="岗位已失效")

    # 文件保存逻辑
    os.makedirs(RESUME_DIR, exist_ok=True)
    unique_filename = f"{uuid.uuid4()}_{resume.filename}"
    file_path = os.path.join(RESUME_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await resume.read())

    # 数据入库
    new_record = ApplicationRecord(
        applicant_name=applicant_name, applicant_email=applicant_email,
        applicant_phone=applicant_phone, job_position_id=job_id,
        resume_path=f"/{file_path.replace(os.path.sep, '/')}"
    )
    session.add(new_record)
    session.commit()

    # 提交成功后重定向 (Post-Redirect-Get 模式)
    # 添加后台任务
    background_tasks.add_task(write_application_to_excel, new_record.id)
    return RedirectResponse(url=request.url_for('get_success_page'), status_code=303)
   