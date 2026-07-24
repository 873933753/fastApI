# web目录放路由
# models目录放模型设计，用来建表
# libs - 辅助函数
# setting文件 - 常用变量

# 1、确认本地数据库已经连接

# 2、确认redis已连接
## 1）启动docker中的redis-dev容器
## 2）连接redis - docker exec -it redis-dev redis-cli - 暂时不用

# 3、启动项目
## 1）cd fisher
## 2）激活虚拟环境 
## 3）启动命令  .\venv\Scripts\python.exe index.py


# 安装包需要写入requirements.txt
```
pip freeze | findstr python-multipart
```

# 启动无法加载检查端口是否被占用
```
reload=True 时 uvicorn 会起 两个进程：

父进程：文件监听（reloader）
子进程：真正跑 FastAPI 的 worker

端口问题-停端口
netstat -ano | findstr ":8000"
Stop-Process -Id 2884 -Force

一键停掉80端口：
在项目目录下打开 PowerShell：
.\stop.ps1 -- Stopped python (PID=21188)
```

# 统一状态码
```
成功：HTTP 200，body.code = 0
业务错误：HTTP 400，body.code = 400
未登录/登录过期：HTTP 401，body.code = 401
参数错误：HTTP 422，body.code = 422
服务端错误：HTTP 500，body.code = 500
第三方服务错误：HTTP 502，body.code = 502

前端处理：
code === 0    成功
code === 401  跳登录
其他 code     直接 toast message

业务异常：AppError抛出来
成功返回：ApiResponse格式返回

业务错误：AppError 默认改为业务错误：code=400、HTTP 400。
成功返回：成功响应统一使用 ApiResponse 默认 code=0，

全局异常处理统一：
参数错误：422
数据写入错误：400
数据库/服务端错误：500
HTTP 异常：body code 等于 HTTP status
保留特殊状态：
未登录/用户不存在登录态：401
发送过于频繁：429

```