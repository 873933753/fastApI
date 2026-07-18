from fastapi import APIRouter

# 创建一个web路由器 - 模块化拆分路由再挂到主app，web_router 统一管理 web/ 下所有路由
# prefix - 设置前缀 /web，所有路由都会以 /web 开头
web_router = APIRouter(prefix='/web')

# 导入book路由
from app.web import book 
from app.web import product
from app.web import test_html
