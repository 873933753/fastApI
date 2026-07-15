# 辅助函数

def is_isbn_or_key(keyword):
  #isbn isbn13 13个0-9的数字组成
  #isbn10 10个0-9的数字组成，包含-符号
  
  is_isbn = 'key'
  # ISBN的判断
  if len(keyword) == 13 and keyword.isdigit():
    is_isbn = 'isbn'
  short_q = keyword.replace('-', '')
  if '-' in keyword and len(short_q) == 10 and short_q.isdigit():
    is_isbn = 'isbn'
  return is_isbn