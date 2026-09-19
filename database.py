from sqlmodel import create_engine

# 定义SQLite数据库路径
DATABASE_URL = "sqlite:///company.db"

# 创建数据库引擎，允许跨线程共享连接
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session