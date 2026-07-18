from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.errors import register_exception_handlers

from pathlib import Path
from fastapi.staticfiles import StaticFiles

# 在应用启动和关闭时初始化和关闭数据库
@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import init_db
    init_db()  # 开发阶段可用；生产建议用 Alembic
    yield

def create_app():
  app = FastAPI(lifespan=lifespan)
  register_exception_handlers(app)
  register_apirouter(app)

  # 注册静态文件路由 - 用于访问静态文件,如图片
  static_dir = Path(__file__).parent / "static"
  app.mount("/static", StaticFiles(directory=static_dir), name="static")

  # app/web/static → /web/static
  web_static_dir = Path(__file__).parent / "web" / "static"
  app.mount("/web/static", StaticFiles(directory=web_static_dir), name="web_static")

  return app

# 注册web路由
def register_apirouter(app):
  from app.web import web_router
  app.include_router(web_router)
