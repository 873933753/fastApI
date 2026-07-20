from typing import Annotated, Any

from fastapi import Query
from pydantic import StringConstraints

from app.libs.helper import is_isbn_or_key
from app.schemas.product import ProductSearchData, ProductItem
from app.schemas.response import ApiResponse
from app.setting import DEFAULT_PAGE_SIZE, PAGE_SIZE_MAX, PAGE_SIZE_MIN
from app.spider.yushu_product import YuShuProduct
from app.view_models.product import ProductCollectionViewModel, ProductViewModel
from . import web_router

SearchQuery = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=30),
    Query(..., description='搜索关键字或 ISBN'),
]

Page = Annotated[int, Query(ge=1, le=999, description='页码，默认 1')]

PageSize = Annotated[
    int,
    Query(ge=PAGE_SIZE_MIN, le=PAGE_SIZE_MAX, description='每页条数'),
]


@web_router.get('/product/search', response_model=ApiResponse[ProductSearchData])
def search(
    q: SearchQuery,
    page: Page = 1,
    size: PageSize = DEFAULT_PAGE_SIZE,
):
    yushu_product = YuShuProduct()
    isbn_or_key = is_isbn_or_key(q)

    if isbn_or_key == 'isbn':
        yushu_product.search_by_isbn(q)
    else:
        yushu_product.search_by_keyword(q, page, size)

    products = ProductCollectionViewModel()
    products.fill(yushu_product, q, page, size)
    return ApiResponse(data=products.data)


# 详情接口 - 通用返回类型
@web_router.get('/product/detail/{isbn}', response_model=ApiResponse[Any])
def detail(isbn: str):
    yushu_product = YuShuProduct()
    yushu_product.search_by_keyword(isbn)
    record = yushu_product.first # 获取第一条数据
    # 查不到 → 空数组   
    if not record:
        return ApiResponse(data={})   # 查不到 → 空对象
    # 查到 → 转换为 ProductItem
    product = ProductViewModel.from_record(record)
    return ApiResponse(data=product)