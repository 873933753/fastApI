from http_client import HTTP

import os
from dotenv import load_dotenv
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
  

  @classmethod
  def search_by_isbn(cls, isbn):
    url = cls.isbn_url.format(isbn=isbn, appKey=APP_KEY)
    return HTTP.get(url)

  @classmethod
  def search_by_keyword(cls, keyword, page=1, size=10):
    url = cls.keyword_url.format(keyword=keyword, page=page, size=size, appKey=APP_KEY)
    return HTTP.get(url)