from typing import List, Union

from pydantic import BaseModel, Field
from app.libs.helper import FormattedDateTime


class ProductItem(BaseModel):
    id: str
    productName: str
    productSubtitle: str = ''
    salePrice: Union[str, float, int] = ''
    orgPrice: float = 0
    stock: int = 0
    image: str = ''
    isbn: str


class ProductSearchData(BaseModel):
    keyword: str
    page: int
    size: int
    total: int
    pages: int = 0
    type: str = Field(description='single 或 list')
    items: List[ProductItem]

class ProductListData(BaseModel):
    page: int
    size: int
    total: int
    pages: int = 0
    items: List[ProductItem]

class HomeGiftItem(ProductItem):
    create_time: FormattedDateTime
