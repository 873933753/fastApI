import asyncio
import time
from fastapi import FastAPI

app = FastAPI()

@app.get("/async")
# 定义异步函数
async def async_func():
  print("async_func start")
  start_time = time.time()
  # 这是异步的同步写法
  # await asyncio.sleep(1)  # 
  # await asyncio.sleep(1)  # 
  # await asyncio.sleep(1)  # 
  # await asyncio.sleep(1)  #
  # await asyncio.sleep(1)  # 

  # 这是异步的异步写法，5个sleep并发执行
  await asyncio.gather(
        asyncio.sleep(1),
        asyncio.sleep(1),
        asyncio.sleep(1),
        asyncio.sleep(1),
        asyncio.sleep(1),
  )
  # f-string 格式化输出
  end_time = time.time()
  print(f"异步时长: {end_time - start_time}")
  return {"message": "异步时长: " + str(end_time - start_time)}

# asyncio.run(async_func())

""" 
打印结果：
async_func start
异步时长: 1.0053486824035645
"""

@app.get("/sync")
# 同步函数
def sync_func():
  print("sync_func start")
  start_time = time.time()
  time.sleep(1)
  time.sleep(1)
  time.sleep(1)
  time.sleep(1)
  time.sleep(1)
  end_time = time.time()
  print(f"同步时长: {end_time - start_time}")
  return {"message": "同步时长: " + str(end_time - start_time)}

# sync_func()

""" 
打印结果：
sync_func start
同步时长: 5.044370174407959
"""
# __name__ 是 Python 中的一个特殊变量，用于表示当前模块的名称。
# 如果当前模块是主程序，则 __name__ 的值为 "__main__"。
if __name__ == "__main__":
  import uvicorn  
  # 运行 FastAPI 应用
  # "async:app" 表示当前模块为 async.py，应用实例为 app
  uvicorn.run("async:app", host="127.0.0.1", port=8002, reload=True)