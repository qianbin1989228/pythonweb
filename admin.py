from sqladmin import ModelView
from models.company import CompanyInfo

class CompanyInfoAdmin(ModelView, model=CompanyInfo):
    """公司信息后台管理视图"""
    column_list = [CompanyInfo.id, CompanyInfo.overview_title]
    # 定义列表页显示的中文名称
    column_labels = {
        CompanyInfo.id: "编号",
        CompanyInfo.overview_title: "简介标题"
    }
    name = "公司信息"
    name_plural = "公司信息"
    icon = "fa-solid fa-house"
    
    
from models.news import News

class NewsAdmin(ModelView, model=News):
    column_list = [News.id, News.title, News.created_at]
    column_labels = {News.id: "编号", News.title: "新闻标题",News.created_at:"发布时间"}
    form_args = {"title": {"label": "新闻标题"}, "content": {"label": "新闻正文"}}
    
    # 指定使用自定义模板以加载TinyMCE
    create_template = "sqladmin/create.html"
    edit_template = "sqladmin/create.html"
    name = "新闻动态"
    name_plural = "新闻动态"
    icon = "fa-solid fa-newspaper"
    

from models.product import Product
from models.product_category import ProductCategory

class ProductCategoryAdmin(ModelView, model=ProductCategory):
    column_list = [ProductCategory.id, ProductCategory.name]
    column_labels = {ProductCategory.id: "编号", ProductCategory.name: "类别名称"}
    name = name_plural = "产品类别"
    icon = "fa-solid fa-tags"

class ProductAdmin(ModelView, model=Product):
    # 直接使用Product.category实现跨表显示类别名称
    column_list = [Product.id, Product.name, Product.category]
    column_labels = {Product.id: "编号", 
                     Product.name: "产品名称", 
                     Product.category: "所属类别"}
    form_args = {"name": {"label": "产品名称"}, 
                 "content": {"label": "产品详情"}, 
                 "category": {"label": "所属类别"}}
    
    # 启用富文本编辑器
    create_template = "sqladmin/create.html"
    edit_template = "sqladmin/create.html"
    name = name_plural = "产品"
    icon = "fa-solid fa-box-archive"
    
    
from models.job_position import JobPosition
from models.application_record import ApplicationRecord
from wtforms.fields import SelectField

# 自定义布尔选择字段，用于激活/禁用状态
class BooleanSelectField(SelectField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [(True, '激活'), (False, '禁用')]
        kwargs['coerce'] = bool
        super().__init__(*args, **kwargs)

class JobPositionAdmin(ModelView, model=JobPosition):
    column_list = [JobPosition.id, JobPosition.title, JobPosition.department, 
                      JobPosition.is_active]
    column_labels = {JobPosition.id: "编号", JobPosition.title: "职位名称", 
                     JobPosition.department: "所属部门", 
                     JobPosition.is_active: "是否激活"}
    form_overrides = {"is_active": BooleanSelectField}
    create_template = "sqladmin/create.html"
    edit_template = "sqladmin/create.html"
    name = name_plural = "招聘岗位"
    icon = "fa-solid fa-briefcase"

class ApplicationRecordAdmin(ModelView, model=ApplicationRecord):
    can_create = False  # 设置为只读
    can_edit = False
    column_list = [ApplicationRecord.id, ApplicationRecord.applicant_name, 
                   ApplicationRecord.job_position, ApplicationRecord.applied_at]
    column_labels = {ApplicationRecord.id: "编号", 
                     ApplicationRecord.applicant_name: "姓名", 
                     ApplicationRecord.job_position: "应聘岗位", 
                     ApplicationRecord.applied_at: "投递时间"}
    name = name_plural = "应聘记录"
    icon = "fa-solid fa-file-lines"
    
    
from models.api_user import ApiUser

class ApiUserAdmin(ModelView, model=ApiUser):
    column_list =[ApiUser.id, ApiUser.username, ApiUser.api_key, 
                  ApiUser.daily_api_calls_left]
    column_labels = {
        ApiUser.id: "编号", 
        ApiUser.username: "API用户名", 
        ApiUser.api_key: "API密钥", 
        ApiUser.daily_api_calls_left: "今日剩余次数"
    }
    can_create = False
    can_edit = False
    name = name_plural = "API 用户"
    icon = "fa-solid fa-user-tag"