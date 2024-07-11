# line_api

使用 FastAPI + SQLModel + SQLAlchemy + MySQL + Alembic 构建的后端基础框架

## Features

- **[FastAPI](https://fastapi.tiangolo.com/)** (Python 3.11)
  - 使用 [OAuth2 "password flow"](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/) 和 AuthLib JWT 令牌进行 JWT 认证

- **[MySQL](https://www.mysql.com/)** 作为数据库
- **[SqlAlchemy](https://www.sqlalchemy.org/)** 作为 ORM
- **[SQLModel](https://sqlmodel.tiangolo.com/)** 结合了 Pydantic 2.x 和 SQLAlchemy 的功能，用于简化数据库模型的定义和操作
- **[Alembic](https://alembic.sqlalchemy.org/en/latest/)** 进行数据库迁移
- **[Pytest](https://docs.pytest.org/en/latest/)** 用于后端测试
  - 包括测试数据库、每个测试后的事务回滚，以及可重用的 [Pytest fixtures](#fixtures)
- **[Celery](http://www.celeryproject.org/)** 用于 [后台任务](#background-tasks) 和 [Redis](https://redis.io/) 作为消息代理
  - 包括用于任务监控的 [Flower](https://flower.readthedocs.io/en/latest/)


## 版本依赖

1.更新依赖文件  
`pip freeze > ./requirements.txt`

2.安装依赖(国内镜像源加速)  
`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

3.执行main.py文件  
`python main.py`

## Alembic数据库迁移工具常用命令

初始化迁移  
`alembic init alembic`  
 
降级  
`alembic downgrade 版本号`  
 
测试  
`alembic -c alembic.ini --name dev revision --autogenerate -m 0.0.1`  

`alembic --name dev upgrade head`  

