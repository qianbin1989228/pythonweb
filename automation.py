import os
import openpyxl
from openpyxl.styles import Font, Alignment
from sqlmodel import Session
from sqlalchemy.orm import selectinload
from database import engine
from models.application_record import ApplicationRecord

REPORT_DIR = "static/reports"
EXCEL_FILE = os.path.join(REPORT_DIR, "applications.xlsx")

def write_application_to_excel(record_id: int):
    # 使用独立会话避免影响主请求
    with Session(engine) as session:
        record = session.get(ApplicationRecord, record_id, 
                             options=[selectinload(ApplicationRecord.job_position)])
        if not record:
            return

        os.makedirs(REPORT_DIR, exist_ok=True)
        headers = ["投递 ID", "姓名", "邮箱", "电话", "应聘岗位", "简历路径", "投递时间"]

        if not os.path.exists(EXCEL_FILE):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "应聘记录"
            sheet.append(headers)
            for cell in sheet[1]:
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center')
        else:
            workbook = openpyxl.load_workbook(EXCEL_FILE)
            sheet = workbook.active

        job_title = record.job_position.title if record.job_position else "N/A"
        row_data = [
            record.id, record.applicant_name, record.applicant_email,
            record.applicant_phone, job_title, record.resume_path,
            record.applied_at.strftime("%Y-%m-%d %H:%M:%S")
        ]
        
        sheet.append(row_data)
        workbook.save(EXCEL_FILE)