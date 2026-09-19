from fastapi.templating import Jinja2Templates

# 创建一个集中的Jinja2Templates实例
templates = Jinja2Templates(directory="templates")

from datetime import datetime, timezone, timedelta

def format_local_time(utc_dt: datetime, fmt: str = "%Y-%m-%d %H:%M") -> str:
    if not isinstance(utc_dt, datetime):
        return ""
    beijing_tz = timezone(timedelta(hours=8))
    local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(beijing_tz)
    return local_dt.strftime(fmt)

# 注册过滤器
templates.env.filters['format_local_time'] = format_local_time

from markupsafe import Markup

def highlight_search_term(text: str, term: str) -> Markup:
    if not term or not text:
        return text
    # 将匹配词替换为带有样式的HTML标签
    highlighted = text.replace(term, f'<span class="text-danger fw-bold">{term}</span>')
    return Markup(highlighted)

templates.env.filters['highlight'] = highlight_search_term