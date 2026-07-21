from fastapi import APIRouter, Depends,Query
from app.schemas.response import ApiResponse
from typing import Any, Annotated
from app.models.user import User
from app.libs.auth import get_current_user
from app.database import get_session, auto_commit
from sqlmodel import Session
from app.models.gift import Gift
from app.setting import BEAN_PER_GIFT
from pydantic import BaseModel, Field
from app.libs.exceptions import AppError
from app.view_models.gift import MyGiftData, MyGifts

# 子路由：/gift 前缀 + 全局鉴权
gift_router = APIRouter(
    prefix='/gift',
    # 可以在该 router 下所有接口添加依赖，如：Depends(get_current_user)
    # 路由级：整组接口都要登录
    dependencies=[Depends(get_current_user)],  # 该 router 下所有接口都要登录
)

CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentSession = Annotated[Session, Depends(get_session)]


# 添加商品到赠送清单请求体
class SaveGiftBody(BaseModel):
    isbn: str = Field(..., min_length=1, max_length=15)
# 将商品添加到赠送清单
@gift_router.post('/product', response_model=ApiResponse[Any])
def save_to_gifts(
  body: SaveGiftBody,
  current_user: CurrentUser,
  session: CurrentSession,
  # isbn: str = Query(..., description='商品isbn'),
  
):
  # # 先要判断是否存在该商品
  # # 既不在赠送清单，也不在心愿清单才能添加

  # # 1）判断是否存在该商品
  # yushu_product = YuShuProduct()
  # yushu_product.search_by_keyword(keyword=isbn)
  # record = yushu_product.first # 获取第一条数据
  # if not record:
  #   return ApiResponse(data={},message='商品不存在',code=400)

  # # 2）判断赠送清单中是否存在该商品,用 user_id + isbn 查 Gift 表
  # gift = session.exec(
  #   select(Gift).where(
  #     Gift.user_id == current_user.id,
  #     # 字典取值用[] 或 .get()
  #     Gift.isbn == record.get('productName'),
  #     Gift.launched == False
  #   )
  # # 执行查询,获取第一条数据
  # ).first()

  # # 3）判断心愿清单中是否存在该商品
  # wish = session.exec(
  #   select(Wish).where(
  #     Wish.user_id == current_user.id,
  #     Wish.isbn == record.get('productName'),
  #     Wish.launched == False
  #   )
  # ).first()

  # # 如果已经在赠送清单或心愿清单中，则不添加
  # if wish or gift:
  #   return ApiResponse(data={},message='这个商品已在赠送清单或心愿清单中，请不要重复添加',code=400)


  # 优化后：使用User模型的can_save_to_list方法判断是否可以添加到赠送清单或心愿清单
  isbn = body.isbn
  # print(current_user.can_save_to_list(session, isbn))
  if current_user.can_save_to_list(session, isbn):
    gift = Gift(
      user_id=current_user.id,
      isbn=isbn
    )
    with auto_commit(session):
      session.add(gift)
      current_user.beans += BEAN_PER_GIFT
    return ApiResponse(data={},message='添加成功',code=200)
  else:
    # return ApiResponse(data={},message='这个商品已在赠送清单或心愿清单中，请不要重复添加',code=400)
    raise AppError(message='这个商品已在赠送清单或心愿清单中，请不要重复添加', code=400, http_status=400)

  # # 添加到gift表 - 提交带数据库中
  # gift = Gift(
  #   user_id=current_user.id,
  #   isbn=record.get('productName')
  # )

  # # 处理回滚事务
  # # bad = Gift(user_id=999999999, isbn="1234567890123")  # 不存在的用户 - 用于测试数据库回滚
  # with auto_commit(session):
  #   session.add(gift)
  #   # 用户每添加一次，获取50 bean
  #   current_user.beans += BEAN_PER_GIFT

  # product = ProductViewModel.from_record(record)
  # return ApiResponse(data=product,message='添加成功',code=200) # 返回商品信息


# 获取当前用户的赠送清单
@gift_router.get('/myList', response_model=ApiResponse[MyGiftData])
def get_gifts(session: CurrentSession, current_user: CurrentUser):
  gifts = Gift.my_gifts(session, current_user.id)
  # 获取每个礼物的isbn列表
  isbn_list = [gift.isbn for gift in gifts]
  # 获取每个礼物的想要人数
  wish_counts_list = Gift.get_wish_count(session, isbn_list)
  wish_count = {item["isbn"]: item["count"] for item in wish_counts_list}

  return ApiResponse(data=MyGifts(gifts, wish_count).to_schema())