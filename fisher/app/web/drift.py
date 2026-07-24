from fastapi import APIRouter, Depends, Body
from app.libs.auth import get_current_user
from app.database import get_session
from sqlmodel import Session
from typing import Annotated, List
from app.models.user import User
from app.schemas.response import ApiResponse
from app.models.gift import Gift
from app.forms.drift import DriftForm
from app.models.drift import Drift
from app.view_models.drift import DriftCollectionViewModel
from app.schemas.pagination import PageData
from app.schemas.drift import DriftItem
from app.schemas.pagination import Page, PageSize, DEFAULT_PAGE_SIZE, paginate
from app.libs.enums import DriftStatus
from app.database import auto_commit
from app.models.wish import Wish
from sqlmodel import select

drift_router = APIRouter(
  prefix='/drift',
  dependencies=[Depends(get_current_user)],
)

CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentSession = Annotated[Session, Depends(get_session)]

# 索要逻辑===============================================
# 判断能否索要：
# 1. 自己的礼物不能索要
# 2、鱼豆要 > 1
# 3、每索取两个商品必须送出一本
@drift_router.get('/can_request', response_model=ApiResponse[dict])
def can_request(
  gift_id: int,
  session: CurrentSession,
  current_user: CurrentUser,
):
  # 根据gift_id查user
  current_gift = session.get(Gift, gift_id)
  if not current_gift:
    return ApiResponse(data={},message='礼物不存在',code=400)

  # 1、自己的书不能索要
  if current_gift.is_yourself_gift(current_user.id):
    return ApiResponse(data={},message='不能索要自己的书',code=400)

  # 2、鱼豆要 > 1
  if not current_user.can_request_gift_beans():
    return ApiResponse(data={},message='鱼豆不足',code=400)

  # 3、每索取两边必须送出一本
  if not current_user.can_request_gift_more(session):
    return ApiResponse(data={},message='每索取两边必须送出一本',code=400)

  # model_dump()：将模型转换为字典
  user = current_gift.user.summary

  return ApiResponse(data=user, message='可以索要')

# 提交索要表单
@drift_router.post('/save_drift', response_model=ApiResponse[dict])
def save_drift(
  form: DriftForm,
  session: CurrentSession,
  current_user: CurrentUser,
):
  from app.models.drift import Drift
  from app.database import auto_commit
  from app.view_models.product import ProductViewModel

  current_gift = session.get(Gift, form.gift_id)
  if not current_gift:
    return ApiResponse(data={}, message='礼物不存在', code=400)

  current_product = ProductViewModel.from_record(current_gift.book)

  if not current_user.can_request_gift_beans():
    return ApiResponse(data={},message='鱼豆不足',code=400)

  # 3、每索取两边必须送出一本
  if not current_user.can_request_gift_more(session):
    return ApiResponse(data={},message='每索取两边必须送出一本',code=400)

  drift = Drift(
    recipient_name=form.recipient_name,
    mobile=form.mobile,
    message=form.message,
    address=form.address,
    gift_id=current_gift.id,
    gifter_id=current_gift.user_id,
    gifter_nickname=current_gift.user.nickname,
    requester_id=current_user.id,
    requester_nickname=current_user.nickname,
    # 商品信息 - 这里不是字典，而是对象，或者用怕productViewModel
    product_title=current_product.productName,
    isbn=current_product.isbn,
    product_img=current_product.image,
    # status=DriftStatus.Waiting,
  )

  # 扣除鱼豆，严谨一些需要判断鱼豆是否足够 -- 后续优化
  current_user.beans -= 1

  with auto_commit(session):
    session.add(drift)

  return ApiResponse(data={},message='索要成功，请等待对方确认',code=200)


# 交易记录列表====================================
@drift_router.post('/drift_list', response_model=ApiResponse[PageData[DriftItem]])
def drift_list(
  session: CurrentSession,
  current_user: CurrentUser,
  page: Annotated[int, Body(ge=1, le=999)] = 1,
  size: Annotated[int, Body(ge=1, le=999)] = DEFAULT_PAGE_SIZE
):
  stmt = Drift.get_drift_list(current_user.id)
  drifts, total = paginate(session, stmt, page, size)
  items = DriftCollectionViewModel(drifts, current_user.id).items
  return ApiResponse(
        data=PageData.build(items, total, page, size),
        code=200,
    )

# 撤销索要 - status为1可撤销
@drift_router.post('/request/redraw', response_model=ApiResponse[dict])
def request_redraw(
  # ge - 大于等于1
  drift_id: Annotated[int, Body(embed=True, ge=1)],
  session: CurrentSession,
  current_user: CurrentUser,
):
  # 防止超权行为，只能撤销自己的索要
  # if drift.requester_id != current_user.id:
  #   return ApiResponse(data={},message='无权限撤销',code=400)

  # drift = session.get(Drift, drift_id)
  from sqlmodel import select
  # 防止超权行为，只能撤销自己的索要
  drift = session.exec(select(Drift).where(Drift.id == drift_id, Drift.requester_id == current_user.id)).first()

  if not drift:
    return ApiResponse(data={},message='交易不存在',code=400)
  if drift.status != DriftStatus.Waiting:
    return ApiResponse(data={},message='当前状态不能撤销',code=400)

  with auto_commit(session): 
    drift.status = DriftStatus.Redraw
    # 返还鱼豆
    current_user.beans += 1

  return ApiResponse(data={},message='撤销成功',code=200)


# 拒绝索要 - status为1可拒绝
@drift_router.post('/request/reject', response_model=ApiResponse[dict])
def request_reject(
  drift_id: Annotated[int, Body(embed=True, ge=1)],
  session: CurrentSession,
  current_user: CurrentUser,
):
  from sqlmodel import select
  drift = session.exec(select(Drift).where(Drift.id == drift_id, Drift.gifter_id == current_user.id)).first()
  if not drift:
    return ApiResponse(data={},message='交易不存在',code=400)
  if drift.status != DriftStatus.Waiting:
    return ApiResponse(data={},message='当前状态不能拒绝',code=400)

  # 返还鱼豆
  user = User.get_user_by_id(session, drift.requester_id)
  user.beans += 1

  with auto_commit(session):
    drift.status = DriftStatus.Redraw
  return ApiResponse(data={},message='拒绝成功',code=200)


# 确认已邮寄 mailed
@drift_router.post('/request/mailed/{drift_id}',response_model=ApiResponse[dict])
def request_mailed(
  drift_id:str,
  session: CurrentSession,
  current_user: CurrentUser
):
 # 先查订单状态
 from sqlmodel import select 
 drift = session.exec(
   select(Drift).where(
     Drift.id == drift_id,
     Drift.gifter_id == current_user.id,
     Drift.status == DriftStatus.Waiting
   )
 ).first()
 if not drift:
   return ApiResponse(data={},message='当前状态不能邮寄',code=400)

 # 商品状态修改为已赠送
 gift = Gift.get_gift_by_id(session, drift.gift_id)
 
 # 更新心愿清单
 wish = Wish.get_wish_by_user(session, gift.isbn,drift.requester_id)
 
 with auto_commit(session):
    drift.status = DriftStatus.Success
    current_user.beans += 1
    gift.launched = True
    wish.launched = True
 return ApiResponse(data={},message='确认成功',code=200)


# 向他赠送逻辑===============================================
@drift_router.get('/can_send', response_model=ApiResponse[dict])
def give(
  isbn: str,
  wish_id: int,
  session: CurrentSession,
  current_user: CurrentUser,
):
  gift = Gift.get_gift_by_user_and_isbn(session, current_user.id, isbn)
  # wish可能被撤销
  wish = session.exec(select(Wish).where(Wish.isbn == isbn, Wish.launched == False,Wish.id == wish_id)).first()
  if not wish:
    return ApiResponse(data={},message='心愿不存在',code=400)
  if not gift or gift.launched:
    return ApiResponse(data={},message='无法赠送',code=400)
  # 成功 - 给该用户发送请求页的邮件进项申请
  return ApiResponse(data={},message='可以赠送',code=200)