from helper import is_isbn_or_key
from yushu_book import YuShuBook
from . import web_router 


@web_router.get('/book/search')
def search(q: str, page: int):
  """ 
  ISBN搜索接口：https://data.isbn.work/openApi/getInfoByIsbn?isbn=9787115611833&appKey=
  关键字搜索接口：https://data.isbn.work/openApi/book/page?current=1&size=10&bookName=活着&appKey
  q - 关键字和ISBN
  page - 页码
  """
  isbn_or_key = is_isbn_or_key(q)
  if isbn_or_key == 'isbn':
    result = YuShuBook.search_by_isbn(q)
  else:
    result = YuShuBook.search_by_keyword(q, page)

  return result