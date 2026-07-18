from app.libs.http_client import HTTP

import os
from dotenv import load_dotenv
from app.setting import DEFAULT_PAGE_SIZE


# 加载环境变量
load_dotenv()
# 获取环境变量
APP_KEY = os.getenv('AppKey')

# 这里是根据关键字和ISBN搜索图书的类
class YuShuBook:
  # isbn_url = 'https://data.isbn.work/openApi/getInfoByIsbn?isbn={isbn}&appKey={appKey}'
  # keyword_url = 'https://data.isbn.work/openApi/book/page?current={page}&size=10&bookName={keyword}&appKey={appKey}'

  isbn_url = 'https://front.zstcwx.cn/api/sysAboutUs/findInfo?isbn={isbn}&appKey={appKey}'
  keyword_url = 'https://front.zstcwx.cn/api/sysAboutUs/findInfo?current={page}&size={size}&bookName={keyword}&appKey={appKey}'
  
  # 初始化书籍信息
  def __init__(self):
    self.total = 0
    self.books = []

  # __是私有方法
  def __fill_single(self,data):
    if data:
      self.total = 1
      self.books.append(data)

  def __fill_collection(self,data):
    self.total = data['total']
    self.books = data['records']

  def search_by_isbn(self, isbn):
    url = self.isbn_url.format(isbn=isbn, appKey=APP_KEY)
    result = HTTP.get(url)
    self.__fill_single(result)

  def search_by_keyword(self, keyword, page=1, size=DEFAULT_PAGE_SIZE):
    url = self.keyword_url.format(keyword=keyword, page=page, size=size, appKey=APP_KEY)
    result = HTTP.get(url)
    self.__fill_collection(result)