from sqlmodel import Field
from typing import Optional
from app.models.base import BaseModel
from sqlalchemy import Column, String

""" 
适合加索引的场景：
经常作为查询条件的字段（如 isbn、用户 ID）
经常用于 WHERE、ORDER BY、JOIN 的字段
索引也有代价：写入、更新、删除时要维护索引，会稍微慢一点，并多占一点存储。
 """

class User(BaseModel, table=True):
  # 表明默认是user，这里改成user1
  # __tablename__ = 'user1'
  # index=True 索引 索引：解决“查得快不快”-什么时候需要 index=True
  #  - 唯一，unique=True — 避免重复
  # primary_key=True 的主键默认就有索引，一般不需要再写 index=True
  id: Optional[int] = Field(default=None, primary_key=True)
  nickname: str = Field(max_length=24)
  phone_number: Optional[str] = Field(default=None, max_length=18, unique=True)
  email: str = Field(max_length=50, unique=True)
  confirmed: bool = Field(default=False)
  beans: int = Field(default=0)
  send_counter: int = Field(default=0)
  receive_counter: int = Field(default=0)
  wx_open_id: Optional[str] = Field(default=None, max_length=50)
  wx_name: Optional[str] = Field(default=None, max_length=32)
  # 修改password字段为password_hash字段，数据库中是password字段，模型中是password_hash字段
  password_hash: str = Field(
    sa_column=Column("password", String(128), nullable=False)
  )




