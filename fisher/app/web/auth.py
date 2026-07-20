# 登录注册模块
from . import web_router
from app.forms.auth import RegisterForm
from app.schemas.response import ApiResponse
from app.models.user import User
from sqlmodel import Session
from app.database import get_session
from fastapi import Depends
from app.libs.security import hash_password
from app.libs.exceptions import AppError    
from sqlmodel import select
from app.schemas.user import UserInfo

""" 
客户端 POST /register
    ↓
FastAPI 用 RegisterForm 解析请求体
    ↓
校验失败 → 抛 RequestValidationError → handlers.py 返回 422
    ↓
校验成功 → 才执行 register(form)
"""

# 注册接口
# response_model - 响应模型，返回用户信息
@web_router.post('/register', response_model=ApiResponse[UserInfo])
def register(form: RegisterForm, session: Session = Depends(get_session)):
  # 检查邮箱是否已注册
  existing = session.exec(
    select(User).where(User.email == form.email)
  ).first()
  if existing:
    raise AppError("电子邮箱已被注册", code=40001)

  # 进入到这里,说明表单验证通过
  # 这里可以进行数据库操作
  data = form.model_dump()
  # 移除password字段 - 防止密码明文存储在数据库中
  plain = data.pop("password")          # 拿走明文
  user = User()
  # 只set其他属性，不set password_hash属性
  user.set_attrs(data)
  user.password_hash = hash_password(plain)
  # 写入数据库
  session.add(user) # 添加到数据库
  session.commit() # 提交数据库
  session.refresh(user) # 刷新数据库，获取最新数据

  # 注册成功 - 返回用户信息
  user_info = UserInfo.model_validate(user)
  return ApiResponse(data=user_info, message="注册成功")

  # 登录接口
  