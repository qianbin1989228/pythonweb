import getpass
from sqlmodel import Session, select
from database import engine
from models.user import User
from auth_utils import hash_password

def create_superuser():
    print("--- 创建超级管理员账户 ---")
    username = input("请输入管理员用户名: ").strip()
    
    # 使用getpass隐藏密码输入
    password = getpass.getpass("请输入管理员密码: ").strip()
    password_confirm = getpass.getpass("请再次确认密码: ").strip()
    
    if password != password_confirm or not password:
        print("密码不一致或为空，创建失败。")
        return

    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.username == 
                        username)).first()
        if existing_user:
            print(f"错误: 用户名 '{username}' 已存在。")
            return
            
        hashed_pwd = hash_password(password)
        new_superuser = User(username=username, hashed_password=hashed_pwd, 
                             is_superuser=True)
        session.add(new_superuser)
        session.commit()
        print(f"成功创建超级管理员账户: {username}")

if __name__ == "__main__":
    create_superuser()