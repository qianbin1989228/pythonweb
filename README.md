# Python Web开发从入门到实战（FastAPI + Bootstrap）- 微课视频版

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)](https://fastapi.tiangolo.com/)
[![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap%205-purple)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **拥抱异步编程，掌握现代全栈开发，集成AI应用，从零构建企业级门户网站。**

> **🌐 在线演示**：本项目完整示例网站已部署上线，欢迎访问 **[www.paisentech.com](http://www.paisentech.com)** 体验最终成品效果！

**作者**：钱彬、沈肖波  
**出版社**：清华大学出版社  
**出版时间**：2025年

---

## 📚 内容简介

本书是一本全面介绍 Python Web 全栈开发的实战教程。区别于传统的 Django/Flask 教程，本书采用了当下性能最强、开发效率最高的 **FastAPI** 框架，结合 **Bootstrap 5** 前端框架，手把手教你构建一个完整的企业级门户网站——“派森科技”。

全书紧扣“实战”二字，摒弃枯燥的 API 罗列，从环境搭建到部署上线，涵盖了 **异步数据库操作 (SQLModel)**、**数据库版本控制 (Alembic)**、**后台管理 (SQLAdmin)**、**JWT 安全认证**、**办公自动化** 以及 **AI 人工智能应用集成** 等核心技术。

💡 **本书特别适合：**
*   Python Web 开发初学者
*   希望从 Django/Flask 转型 FastAPI 的开发者
*   对全栈开发、AI 应用集成感兴趣的技术从业者
*   高校学生及培训机构学员

---

## 🚀 本书特色

*   **技术栈新**：全面拥抱 Python 3.10+ 和异步编程，采用 FastAPI + SQLModel + Pydantic v2。
*   **全栈实战**：不仅讲后端，还涵盖 HTML5/CSS3/JS 和 Bootstrap 5，教你独立完成前后端。
*   **企业级规范**：包含数据库迁移 (Alembic)、ORM 建模、依赖注入、模块化路由设计。
*   **AI 赋能**：书中集成了 **OpenCV** 计算机视觉（二维码解析）与 **大语言模型**（智能客服），紧跟 AI 时代潮流。
*   **办公自动化**：实战讲解如何利用后台任务结合 OpenPyXL 实现数据的异步归档与 Excel 报表生成。
*   **生产部署**：详细讲解 Windows Server 环境下 Nginx + HTTPS 的生产级部署流程。
*   **资源丰富**：提供全程配套教学视频、源代码及所需软件资源。

---

## 🛠️ 技术架构

本项目（派森科技门户网站）采用了以下核心技术栈：

| 领域 | 技术/库 | 说明 |
| :--- | :--- | :--- |
| **后端框架** | **FastAPI** | 高性能异步 Web 框架 |
| **数据库/ORM** | **SQLModel** | 结合 SQLAlchemy 与 Pydantic 的现代化 ORM |
| **数据库迁移** | **Alembic** | 数据库版本控制工具 |
| **前端框架** | **Bootstrap 5** | 响应式 UI 框架，无需深厚 CSS 功底 |
| **模板引擎** | **Jinja2** | 强大的 Python 模板引擎 |
| **后台管理** | **SQLAdmin** | 专为 FastAPI 设计的现代化后台 |
| **安全认证** | **JWT (Passlib)** | 无状态身份认证与密码哈希 |
| **AI/工具** | **OpenCV / LLM** | 计算机视觉与大模型 API 集成 |
| **部署** | **Nginx / Uvicorn** | 反向代理与 ASGI 服务器 |

---

## 📂 章节目录

全书共分为三部分，十二章，循序渐进：

### 第一部分：基础篇
*   **第1章 环境搭建**：Python 环境、虚拟环境、VS Code 配置、第一个 FastAPI 应用。
*   **第2章 基础语法**：Python 核心语法回顾、装饰器、HTML/CSS/JS/Bootstrap 5 基础、实战“在线计算器”。

### 第二部分：开发篇（实战“派森科技”门户）
*   **第3章 项目框架设计**：目录结构规划、模块化路由、静态资源配置。
*   **第4章 开发“公司简介”模块**：模板继承、静态页面动态化。
*   **第5章 开发“后台管理”模块**：SQLModel 建模、集成 SQLAdmin、Alembic 迁移。
*   **第6章 开发“新闻动态”模块**：集成 TinyMCE 富文本编辑器、图片上传、分页实现。
*   **第7章 开发“产品中心”模块**：一对多关系建模、多维筛选、搜索高亮。
*   **第8章 开发“人才招聘”模块**：文件上传、**后台任务**、OpenPyXL 简历自动归档。
*   **第9章 开发“认证系统”模块**：用户模型、JWT 登录/登出、依赖注入权限控制。
*   **第10章 开发“服务支持”模块**：**OpenCV** 二维码解析、API Key 管理、速率限制。
*   **第11章 开发“首页”模块**：服务端缓存 (Redis/Memory)、集成 **大模型 API** 实现智能客服。

### 第三部分：部署篇
*   **第12章 项目上线与部署**：云服务器选购、Windows Server 环境配置、Nginx 反向代理、HTTPS 证书配置。

---

## 💻 源码使用说明

1.  **克隆仓库**
    ```bash
    git clone https://github.com/qianbin1989228/pythonweb.git
    cd pythonweb
    ```

2.  **创建虚拟环境**
    ```bash
    python -m venv venv
    # Windows 激活
    .\venv\Scripts\activate
    # Mac/Linux 激活
    source venv/bin/activate
    ```

3.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

4.  **初始化数据库**
    ```bash
    # 自动生成迁移脚本（如果已有 versions 文件夹可跳过）
    alembic revision --autogenerate -m "init"
    # 执行迁移
    alembic upgrade head
    # 创建超级管理员
    python create_superuser.py
    ```

5.  **运行项目**
    ```bash
    uvicorn main:app --reload
    ```
    访问浏览器：`http://127.0.0.1:8000`  
    API 文档：`http://127.0.0.1:8000/docs`

---

## 🛒 购买链接

*   **京东**：[点击购买](此处替换为您的京东链接)
*   **当当**：[点击购买](此处替换为您的当当链接)
*   **天猫**：[点击购买](此处替换为您的天猫链接)

*(如果您觉得本书对您有帮助，欢迎购买纸质版支持作者！)*

---

## 🤝 交流与反馈

如果您在阅读本书或运行代码时遇到任何问题，欢迎通过以下方式联系：

*   **GitHub Issues**: [提交 Issue](https://github.com/qianbin1989228/pythonweb/issues)
*   **Email**: (645224083@qq.com)
*   **QQ交流群**: (820106877)

---

**Star 🌟 这个仓库，一起探索 Python Web 开发的无限可能！**
