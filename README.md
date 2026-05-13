toutiao_backend/
├── config/                 # 配置文件
│   └── db_conf.py          # 数据库配置
├── crud/                   # 数据访问层（业务数据操作）
│   ├── favorite.py         # 收藏相关操作
│   ├── history.py          # 浏览历史相关操作
│   ├── news.py             # 新闻资讯相关操作
│   └── users.py            # 用户相关操作
├── models/                 # SQLAlchemy ORM 模型
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── users.py
├── routers/                # API 路由定义
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── users.py
├── schemas/                # Pydantic 数据模型与校验
│   ├── base.py
│   ├── favorite.py
│   ├── history.py
│   └── users.py
├── utils/                  # 工具函数
│   ├── auth.py             # 认证与权限工具
│   ├── exception.py        # 自定义异常
│   ├── exception_handlers.py # 全局异常处理
│   ├── response.py         # 统一响应格式
│   └── security.py         # 安全相关工具
├── main.py                 # 项目入口
├── README.md               # 项目说明文档
└── requirements.txt        # 依赖清单
开发环境
Python 3.10+
FastAPI 异步 Web 框架
SQLAlchemy ORM
Pydantic 数据校验

安装 conda（可选）
下载
shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
安装
shell
bash Miniconda3-latest-MacOSX-x86_64.sh

创建虚拟环境
shell
conda create -n toutiao_backend python=3.10
conda activate toutiao_backend

安装依赖
shell
pip install -r requirements.txt

数据库配置
修改 config/db_conf.py 中的数据库连接信息：
python

运行
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/toutiao_db"
初始化数据库
项目使用 SQLAlchemy ORM，可通过 Alembic 进行迁移管理：
shell
# 安装 alembic
pip install alembic

# 初始化 alembic
alembic init alembic
配置 alembic.ini：
ini
script_location = ./alembic
sqlalchemy.url = mysql+pymysql://root:root@127.0.0.1:3306/toutiao_db
修改 alembic/env.py：
python
运行
from models.base import Base
target_metadata = Base.metadata
执行迁移：
shell
alembic upgrade head
启动项目
开发模式（带热重载）：
shell
uvicorn main:app --reload --port 8000
生产模式：
shell
uvicorn main:app --host 0.0.0.0 --port 8000
访问接口文档：
plaintext
http://127.0.0.1:8000/docs
核心模块说明
1. 用户模块
用户注册、登录、JWT 认证
密码加盐加密存储
用户信息管理
2. 新闻资讯模块
头条式新闻浏览、分页查询
新闻分类、热门推荐
新闻详情浏览、内容管理
3. 收藏与历史模块
用户收藏管理（添加 / 取消收藏）
浏览历史记录与查询
4. 通用工具
全局异常处理
统一响应格式封装
权限与认证工具
