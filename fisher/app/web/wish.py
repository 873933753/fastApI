from fastapi import APIRouter, Depends
from app.schemas.response import ApiResponse
from typing import Any, Annotated
from app.models.user import User
from app.libs.auth import get_current_user
from app.database import get_session, auto_commit
from sqlmodel import Session
from pydantic import BaseModel, Field
from app.libs.exceptions import AppError
from app.models.wish import Wish

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
    isbn: str = Field(..., min_length=1, max_length=15)
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