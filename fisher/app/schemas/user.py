from pydantic import BaseModel

# 返回的用户信息模型
class UserInfo(BaseModel):
  id: int
  email: str
  nickname: str
  
  model_config = {"from_attributes": True}  # 允许从 ORM 对象构造 Pydantic 模型