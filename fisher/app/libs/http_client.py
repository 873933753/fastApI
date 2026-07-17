import requests

# 定义一个类，封装 HTTP 请求方法
class HTTP:
  @staticmethod # 静态方法，不需要实例化类就可以调用，调用时参数会按位置一一对应
  def get(url, return_json=True):
    # r 是 requests.get(url) 的响应对象，return_json 默认 True，表示希望按 JSON 解析。
    r = requests.get(url)
    # 如果响应状态码不是 200，则返回空字典或空字符串（原数据格式决定）
    if r.status_code != 200:
      return {} if return_json else ''
    # 如果响应状态码是 200，则返回 JSON 数据或文本数据，取决于 return_json 的值。
    # 三元表达式：return_json=True → r.json() -返回 JSON 数据；
    #return_json=False → r.text -返回文本数据。
    return r.json() if return_json else r.text 
  