from fastapi import FastAPI
from contextlib import asynccontextmanager

# 在应用启动和关闭时初始化和关闭数据库
@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import init_db
    init_db()  # 开发阶段可用；生产建议用 Alembic
    yield

def create_app():
  # 在应用启动和关闭时初始化和关闭数据库
  app = FastAPI(lifespan=lifespan)
  # 注册API路由
  register_apirouter(app)
  return app

# 注册web路由
def register_apirouter(app):
  from app.web import web_router
  app.include_router(web_router)