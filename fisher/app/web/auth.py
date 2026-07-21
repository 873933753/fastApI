# 登录注册模块
from . import web_router
from app.forms.auth import RegisterForm,LoginForm
from app.schemas.response import ApiResponse
from app.models.user import User
from sqlmodel import Session
from app.database import get_session, auto_commit
from fastapi import Depends
from app.libs.security import hash_password,verify_password
from app.libs.exceptions import AppError    
from sqlmodel import select
from app.schemas.user import UserInfo,LoginResult
# 导入生成访问令牌和登录结果模型
from app.libs.security import create_access_token
from app.libs.auth import get_current_user

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
  with auto_commit(session):
    session.add(user) # 添加到数据库

  # 注册成功 - 返回用户信息
  user_info = UserInfo.model_validate(user)
  return ApiResponse(data=user_info, message="注册成功")


# 登录接口
@web_router.post('/login',response_model=ApiResponse[LoginResult])
def login(form: LoginForm, session: Session = Depends(get_session)):
    # 检查邮箱密码是否匹配
    """ 
    1)按邮箱查用户
    2)校验查出来的用户密码是否匹配
    """
    # 1)按邮箱查用户
    user = session.exec(
      select(User).where(User.email == form.email)
    ).first()

    # 2)校验查出来的用户密码是否匹配
    # “用户不存在”和“密码错误”应返回同一条消息（如 "邮箱或密码错误"），降低邮箱枚举风险
    if not user or not verify_password(form.password,user.password_hash):
      raise AppError("邮箱或密码错误",code=40002,http_status=400)
      
    # 邮箱密码匹配 - 登录成功并返回用户信息
    user_info = UserInfo.model_validate(user)

    # 生成访问令牌
    token = create_access_token(user.id)
    return ApiResponse(
        data=LoginResult(token=token, user=user_info),
        message="登录成功"
    ) 

# 验证JWT token的接口
# 使用get_current_user装饰器获取当前用户，返回用户信息，给前端展示用户信息
@web_router.get('/profile', response_model=ApiResponse[UserInfo])
def profile(current_user: User = Depends(get_current_user)):
    return ApiResponse(data=UserInfo.model_validate(current_user))