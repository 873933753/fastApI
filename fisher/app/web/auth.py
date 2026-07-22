# 登录注册模块
from contextlib import redirect_stderr
from . import web_router
from app.forms.auth import RegisterForm,LoginForm
from app.schemas.response import ApiResponse
from app.models.user import User
from sqlmodel import Session
from app.database import get_session, auto_commit
from fastapi import Depends, Request,Form,BackgroundTasks
from app.libs.security import hash_password,verify_password
from app.libs.exceptions import AppError    
from sqlmodel import select
from app.schemas.user import UserInfo,LoginResult
# 导入生成访问令牌和登录结果模型
from app.libs.security import create_access_token
from app.libs.auth import get_current_user
from app.forms.auth import EmailForm,ResetPasswordForm


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
@web_router.get('/profile', response_model=ApiResponse[None])
def profile(current_user: User = Depends(get_current_user)):
    return ApiResponse(data=UserInfo.model_validate(current_user))


# 忘记密码 - 发送重置密码邮件
@web_router.post('/forgetPassword', response_model=ApiResponse[dict])
def forgetPassword(
  form: EmailForm, 
  background_tasks: BackgroundTasks,
  session: Session = Depends(get_session),
):
    user = User.get_user_by_email(session, form.email)
    if not user:
      raise AppError("邮箱不存在", code=40003, http_status=400)
    
    from app.libs.email import send_email_safe
    # 邮箱存在，后台发送重置密码邮件
    reset_url = f'http://127.0.0.1:8000/web/reset/password/{user.generate_token()}'

    background_tasks.add_task(
      send_email_safe,
      # to=form.email,
      to='tang_tk001@outlook.comxxx',
      subject="重置你的密码",
      template="email/reset_password.html",
      user={"email": "亲爱的用户"},
      reset_url=reset_url,
    )
    return ApiResponse(
      data={
        "reset_url": reset_url
      },
      message="已提交发送重置邮件，请查收邮箱"
    )

# 重置密码页面
@web_router.get('/reset/password/{token}')
def reset_password_page(
  token: str,
  request: Request
):
    from app.libs.templates import templates
    return templates.TemplateResponse(
        request=request,
        name="auth/forget_password.html",
        context={
          "request": request,
          "token": token
        }
    )
# post请求，重置密码
# Form接参 + Pydantic 校验
@web_router.post('/reset/password/{token}', response_model=ApiResponse[dict])
def reset_password(
  token: str, 
  new_password: str = Form(...),
  confirm_password: str = Form(...),
  session: Session = Depends(get_session)
):
    # 导入ValidationError-用于处理表单验证错误
    from pydantic import ValidationError
    from fastapi.exceptions import RequestValidationError
    from app.libs.security import decode_reset_token
    try:
    # 这里才会走 ResetPasswordForm 的长度/两次一致等规则
    # 失败 → RequestValidationError → 你们 handlers 返回 422 JSON
      form = ResetPasswordForm(
          new_password=new_password,
          confirm_password=confirm_password,
      )
    except ValidationError as e:
       raise RequestValidationError(e.errors())

    # 2、验证token是否有效
    user = User.validate_token(session, token)

    # 3、重置密码
    user.reset_password(form.new_password, session)

    return ApiResponse(data={},message="密码重置成功")



    # 忘记密码 - 发送邮箱验证码