from sqlmodel import Session, select
from models.company import CompanyInfo
from models.product import Product
from database import engine

def build_company_knowledge_base() -> str:
    prompt_parts = [
        "作为派森科技的智能客服助手，请根据以下资料回答提问。"
        "若超出资料范围，请建议联系人工客服。"
    ]
    
    with Session(engine) as session:
        info = session.exec(select(CompanyInfo)).first()
        if info:
            prompt_parts.append(
                f"\n【公司简介】\n{info.overview_lead_text}"
                f"\n【企业文化】\n{info.culture_intro}"
            )
            
        products = session.exec(select(Product)).all()
        if products:
            prompt_parts.append("\n【产品列表】")
            for p in products:
                # 简单清洗HTML标签
                clean_desc = (
                    p.content.replace("<p>", "")
                    .replace("</p>", "")
                    .replace("&nbsp;", "")
                )
                prompt_parts.append(
                    f"- {p.name} ({p.category.name})：{clean_desc[:150]}..."
                )
                
    return "\n".join(prompt_parts)