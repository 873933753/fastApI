from sqlmodel import SQLModel, Field

# 基类模型 - 所有模型都继承自这个基类
class BaseModel(SQLModel):
  is_deleted: bool = Field(default=False) # 是否删除,默认未删除

  # attrs_dict: 字典，键为属性名，值为属性值
  def set_attrs(self, attrs_dict: dict):
    for key, value in attrs_dict.items():
      # 如果属性存在且不是id，则设置属性 - 往模型中设置属性
      # 只是把属性赋到对象上，并没有写入数据库
      if hasattr(self, key) and key != 'id':
        setattr(self, key, value)