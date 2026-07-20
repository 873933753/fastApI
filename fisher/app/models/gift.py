from sqlmodel import Field
from typing import Optional, TYPE_CHECKING
from sqlmodel import Relationship
from app.models.base import BaseModel

# TYPE_CHECKING - 类型检查，避免循环导入
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.book import Book

# 礼物模型
class Gift(BaseModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  launched: bool = Field(default=False) # 是否赠送,默认未赠送

  # 外键关联用户 - 暂时不做反向关联
  # back_populates='gifts' - 反向关联，用于查询礼物时，查询用户时，查询礼物
  user:Optional['User'] = Relationship()
  # 外键关联用户ID
  user_id: Optional[int] = Field(default=None, foreign_key='user.id')
  
  # 外键关联书籍
  # book:Optional['Book'] = Relationship()
  # # 外键关联书籍ID
  # book_id: Optional[int] = Field(default=None, foreign_key='book.id')

  # 外键关联ISBN - 因为book的isbn是唯一索引，所以可以用isbn关联book
  isbn: Optional[str] = Field(default=None, max_length=15) # ISBN，最大长度15