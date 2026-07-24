from fastapi import APIRouter, Depends
from app.schemas.response import ApiResponse
from typing import Any, Annotated
from app.models.user import User
from app.libs.auth import get_current_user
from app.database import get_session, auto_commit
from sqlmodel import Session
from pydantic import BaseModel, Field
from app.libs.exceptions import AppError
from app.view_models.trade import MyTrades,MyGiftData
from app.models.wish import Wish
from app.schemas.pagination import Page, PageSize, PageData, paginate
from app.setting import DEFAULT_PAGE_SIZE
from app.schemas.product import HomeGiftItem



# 子路由：/gift 前缀 + 全局鉴权
wish_router = APIRouter(
    prefix='/wish',
    # 可以在该 router 下所有接口添加依赖，如：Depends(get_current_user)
    # 路由级：整组接口都要登录
    dependencies=[Depends(get_current_user)],  # 该 router 下所有接口都要登录
)

CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentSession = Annotated[Session, Depends(get_session)]


# 添加商品到心愿清单请求体
class SaveGiftBody(BaseModel):
    isbn: str = Field(..., min_length=1, max_length=50)
# 将商品添加到心愿清单
@wish_router.post('/product', response_model=ApiResponse[Any])
def save_to_gifts(
  body: SaveGiftBody,
  current_user: CurrentUser,
  session: CurrentSession
):
  isbn = body.isbn
  if current_user.can_save_to_list(session, isbn):
    wish = Wish(
      user_id=current_user.id,
      isbn=isbn
    )
    with auto_commit(session):
      session.add(wish)
    return ApiResponse(data={},message='添加成功',code=200)
  else:
    raise AppError(message='这个商品已在赠送清单或心愿清单中，请不要重复添加', code=400, http_status=400)

# 获取当前用户的心愿清单
@wish_router.get('/myList', response_model=ApiResponse[PageData[HomeGiftItem]])
def get_wishes(
  session: CurrentSession,
  current_user: CurrentUser,
  page: Page = 1,
  size: PageSize = DEFAULT_PAGE_SIZE
):
  # 分页查询心愿清单
  # stmt: 查询心愿清单的语句
  stmt = Wish.my_wishes_query(current_user.id)  # 方案 A
  wishes, total = paginate(session, stmt, page, size)

  # wishes = Wish.my_wishes_query(current_user.id)
  isbn_list = [wish.isbn for wish in wishes]
  wish_counts_list = Wish.get_wish_count(session, isbn_list)
  wish_count = {item["isbn"]: item["count"] for item in wish_counts_list}
  my_trades = MyTrades(wishes, wish_count)
  return ApiResponse(
    data=PageData.build(my_trades.items, total, page, size),
    message='获取心愿清单成功'
  )

  # 撤销心愿
@wish_router.post('/request/redraw/{wish_id}', response_model=ApiResponse[dict])
def request_redraw(
  wish_id: int,
  session: CurrentSession,
  current_user: CurrentUser,
):
  wish = Wish.get_wish_by_id(session, wish_id)
  if not wish or wish.launched or wish.user_id != current_user.id:
    return ApiResponse(data={},message='无法撤销',code=400)
  with auto_commit(session):
    wish.soft_delete()
  return ApiResponse(data={},message='撤销成功',code=200)