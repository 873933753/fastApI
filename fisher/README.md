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
## 2）激活虚拟环境 .\venv\Scripts\Activate.ps1
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

# 数据库迁移（Alembic）

改表不要靠启动时 create_all，按下面流程：

1. 修改 `app/models/*.py`
2. 生成迁移：`alembic revision --autogenerate -m "说明这次改了什么"`
3. **打开** `alembic/versions/` 下新文件检查：只保留本次真正需要的变更，删掉误报的 drop/alter
4. 执行：`alembic upgrade head`
5. 提交时：模型文件 + `alembic/versions/xxx.py` 一起提交

常用命令（在 `fisher/` 目录、已激活 venv）：

```powershell
alembic current
alembic upgrade head
alembic downgrade -1