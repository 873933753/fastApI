from fastapi import FastAPI

def create_app():
  app = FastAPI()
  # 注册API路由
  register_apirouter(app)
  return app

# 注册web路由
def register_apirouter(app):
  from app.web import web_router
  app.include_router(web_router)