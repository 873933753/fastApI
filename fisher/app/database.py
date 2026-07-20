# 数据库连接与会话管理
from sqlmodel import SQLModel, create_engine, Session
from app.secure import DATABASE_URL

# SQLite 多线程下需要 check_same_thread=False；MySQL 不需要额外 connect_args
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL and DATABASE_URL.startswith("sqlite")
    else {}
)

# 创建数据库引擎
# echo=True 会在控制台打印 SQL，方便开发调试；上线后可改为 False
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def init_db():
    """应用启动时根据模型自动建表（开发阶段使用，生产建议用 Alembic 迁移）"""
    # 必须导入模型，否则 metadata 中无表定义，create_all 不会建表
    from app.models.book import Book  # noqa: F401
    from app.models.gift import Gift  # noqa: F401
    from app.models.user import User  # noqa: F401
    

    SQLModel.metadata.create_all(engine)

# 获取数据库会话，供路由通过 Depends(get_session) 注入使用
def get_session():
    """
    数据库会话依赖，供路由通过 Depends(get_session) 注入使用。

    用法示例（在路由文件中）：
        from fastapi import Depends
        from sqlmodel import Session
        from app.database import get_session

        @router.get("/book/{isbn}")
        def get_book(isbn: str, session: Session = Depends(get_session)):
            ...

    FastAPI 会在每个请求前创建 Session，请求结束后自动关闭，无需手动 session.close()。
    """
    # 1、with Session(engine) as session：从连接池拿到一个数据库会话（相当于“连接上数据库”）
    # 2、yield session：把 session 交给 FastAPI 路由使用
    # 3、请求结束后：with 块结束，Session 自动 close()，连接归还连接池
    # 所以注释里写“无需手动 session.close()”——with 帮你做了这件事。
    with Session(engine) as session:
        yield session
