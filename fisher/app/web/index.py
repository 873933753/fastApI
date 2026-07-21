from fastapi import Depends
from app.schemas.response import ApiResponse
from app.database import get_session
from app.models.gift import Gift
from typing import Annotated
from sqlmodel import Session
from app.web import web_router
from app.schemas.product import ProductItem, HomeGiftItem
from app.view_models.product import ProductViewModel
from pydantic import BaseModel
from typing import List

CurrentSession = Annotated[Session, Depends(get_session)] 


class HomeGiftData(BaseModel):
    total: int
    items: List[HomeGiftItem]

# 获取赠送清单
@web_router.get('/home/list', response_model=ApiResponse[HomeGiftData])
def get_gifts(session: CurrentSession):
  recent_gifts = Gift.recent_gifts(session)
  # products = [ProductViewModel.from_record(gift.book) for gift in recent_gifts]
  products = [
    HomeGiftItem(
        # * 解包：将ProductViewModel.from_record(gift.book)中的所有字段解包到HomeGiftItem中
        **ProductViewModel.from_record(gift.book).model_dump(),
        create_time=gift.create_time,  # 来自 Gift，不是 book
    )
    for gift in recent_gifts
]
  return ApiResponse(
    data=HomeGiftData(
      total=len(products),
      items=products
    )
  )