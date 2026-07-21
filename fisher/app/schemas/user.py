from pydantic import BaseModel, field_validator
from datetime import datetime, timezone, timedelta

# 东八区
CN_TZ = timezone(timedelta(hours=8))

# 返回的用户信息模型
class UserInfo(BaseModel):
  id: int
  email: str
  nickname: str
  beans: int
  create_time: str
  
  model_config = {"from_attributes": True}  # 允许从 ORM 对象构造 Pydantic 模型

  @field_validator("create_time", mode="before")
  @classmethod
  def ts_to_str(cls, v):
      # ORM 传来的是 int 时间戳（秒）
      if isinstance(v, int):
          return datetime.fromtimestamp(v, tz=CN_TZ).strftime("%Y-%m-%d %H:%M:%S")
      return v

# 登录结果模型
""" 
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "token": "eyJhbG...",
    "user": { "id": 1, "email": "...", "nickname": "..." }
  }
}
"""

class LoginResult(BaseModel):
    token: str
    user: UserInfo