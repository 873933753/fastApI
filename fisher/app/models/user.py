import stat
from sqlmodel import Field
from typing import Optional
from app.models.base import BaseModel
from sqlalchemy import Column, String
from sqlmodel import Session, select
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_product import YuShuProduct
from app.libs.exceptions import AppError

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
  nickname: Optional[str] = Field(default=None, max_length=24)
  phone_number: Optional[str] = Field(default=None, max_length=18, unique=True)
  email: str = Field(max_length=50, unique=True)
  confirmed: bool = Field(default=False)
  beans: int = Field(default=0)
  send_counter: int = Field(default=0)
  receive_counter: int = Field(default=0)
  wx_open_id: Optional[str] = Field(default=None, max_length=50)
  wx_name: Optional[str] = Field(default=None, max_length=32)
  # 修改password字段为password_hash字段，数据库中是password字段，模型中是password_hash字段
  # nullable=False - 不允许为空,Column中的
  password_hash: str = Field(
    sa_column=Column("password", String(128), nullable=False)
  )

  # 判断是否可以添加到赠送清单或心愿清单
  def can_save_to_list(self, session: Session, isbn: str) -> bool:
      # 1）判断是否存在该商品
    yushu_product = YuShuProduct()
    yushu_product.search_by_keyword(keyword=isbn)
    record = yushu_product.first # 获取第一条数据
    if not record:
      # return ApiResponse(data={},message='商品不存在',code=400)
      raise AppError(message='商品不存在', code=40001, http_status=400)

    # 2）判断赠送清单中是否存在该商品,用 user_id + isbn 查 Gift 表
    gift = session.exec(
      select(Gift).where(
        Gift.user_id == self.id,
        # 字典取值用[] 或 .get()
        Gift.isbn == record.get('productName'),
        Gift.launched == False
      )
    # 执行查询,获取第一条数据
    ).first()

    # 3）判断心愿清单中是否存在该商品
    wish = session.exec(
      select(Wish).where(
        # 这里的self是User模型，id是User模型的id字段
        Wish.user_id == self.id,
        Wish.isbn == record.get('productName'),
        Wish.launched == False
      )
    ).first()

    # 如果已经在赠送清单或心愿清单中，则不添加
    if wish or gift:
      return False
    return True


  # 按照邮箱查询用户
  @classmethod
  def get_user_by_email(cls, session: Session, email: str) -> Optional[User]:
    return session.exec(
      select(cls).where(cls.email == email)
    # first_or_none() - 如果查询结果为空，则返回 None
    # first() - 如果查询结果为空，则抛出异常
    ).first()

  # 生成token - 链接上的
  def generate_token(self,expiration: int = 600) -> str:
    from app.libs.security import create_reset_token
    return create_reset_token(self.id, expiration)

  # 验证token是否有效
  @classmethod
  def validate_token(cls, session, token):
      from app.libs.security import decode_reset_token
      user_id = decode_reset_token(token)
      if not user_id:
          raise AppError("token无效", code=40004)
      user = session.get(cls, user_id)
      if not user:
          raise AppError("用户不存在", code=40005)
      return user

  # 重置密码
  def reset_password(self, new_password: str, session: Session) -> None:
    # 1、验证token是否有效
    from app.database import auto_commit
    from app.libs.security import hash_password
    self.password_hash = hash_password(new_password)
    with auto_commit(session):
      session.add(self)




